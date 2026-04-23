from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, tcp, udp

log = core.getLogger()

# MAC learning table
mac_to_port = {}

# Packet counter (for logging)
packet_count = 0


def _handle_PacketIn(event):
    global packet_count

    packet = event.parsed
    if not packet.parsed:
        return

    dpid = event.connection.dpid
    in_port = event.port

    # Initialize table for switch
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC address
    mac_to_port[dpid][packet.src] = in_port

    packet_count += 1

    # ---------------- LOGGING ----------------
    log_msg = "\n=== Packet Captured ===\n"
    log_msg += f"Packet No: {packet_count}\n"

    # Ethernet
    eth = packet.find('ethernet')
    if eth:
        log_msg += f"Ethernet: {eth.src} -> {eth.dst}\n"

    # IP
    ip = packet.find('ipv4')
    if ip:
        log_msg += f"IP: {ip.srcip} -> {ip.dstip} | Protocol: {ip.protocol}\n"

    # TCP
    tcp_pkt = packet.find('tcp')
    if tcp_pkt:
        log_msg += f"TCP: {tcp_pkt.srcport} -> {tcp_pkt.dstport}\n"

    # UDP
    udp_pkt = packet.find('udp')
    if udp_pkt:
        log_msg += f"UDP: {udp_pkt.srcport} -> {udp_pkt.dstport}\n"

    # Print logs
    print(log_msg)

    # Save logs to file
    with open("packet_logs.txt", "a") as f:
        f.write(log_msg + "\n")

    # ---------------- LEARNING SWITCH LOGIC ----------------

    # Check if destination MAC is known
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]
    else:
        out_port = of.OFPP_FLOOD

    actions = [of.ofp_action_output(port=out_port)]

    # Install flow rule if destination is known
    if out_port != of.OFPP_FLOOD:
        match = of.ofp_match.from_packet(packet)
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = match
        flow_mod.actions = actions
        event.connection.send(flow_mod)

    # Send packet out
    packet_out = of.ofp_packet_out()
    packet_out.data = event.ofp
    packet_out.actions = actions
    packet_out.in_port = in_port
    event.connection.send(packet_out)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Packet Logger + Learning Switch Started 🚀")
