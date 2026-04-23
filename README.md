 Packet Logger using SDN Controller (POX)

Problem Statement

Design and implement a Software Defined Networking (SDN) application that captures packets traversing the network using controller events, identifies protocol types, logs packet information, and demonstrates forwarding using flow rules.


 Objective

* Capture packets using SDN controller (POX)
* Identify protocol details (Ethernet, IP, TCP/UDP)
* Maintain logs of captured packets
* Demonstrate packet forwarding using flow rules (learning switch)


Tools & Technologies

* Mininet – Network emulation
* POX Controller – SDN controller
* Ubuntu 22.04 – Development environment
* Python – Controller logic

---

Network Topology

* 1 Switch (s1)
* 3 Hosts (h1, h2, h3)
* Hosts connected to switch via virtual links

How It Works

1. Packet Arrival

   * When a packet arrives at the switch without a matching rule, it is sent to the controller (PacketIn event).

2. Packet Processing

   * The controller extracts:

     * Ethernet header
     * IP header
     * Transport layer (TCP/UDP)

3. Logging

   * Packet details are:

     * Displayed in terminal
     * Stored in `packet_logs.txt`

4. Learning Switch Mechanism

   * Controller learns MAC-to-port mapping
   * Installs flow rules (match–action)
   * Subsequent packets are forwarded directly by switch

Execution Steps

### Step 1: Start POX Controller

```bash
cd ~/pox
./pox.py misc.packet_logger
```

### Step 2: Start Mininet

```bash
sudo mn -c
sudo mn --controller=remote,ip=127.0.0.1 --topo single,3
```

### Step 3: Test Connectivity

```bash
pingall
```

---

## ✅ Expected Output

* All hosts communicate successfully
* Output:

```
Results: 0% dropped
```

* Controller displays logs:

```
=== Packet Captured ===
Ethernet: ...
IP: ...
TCP/UDP: ...
```

* Logs stored in:

```
packet_logs.txt
```

---

## 📊 Sample Output

Refer to:

* `screenshots/` for execution proof
* `sample_logs/packet_logs_sample.txt` for captured logs

---

## 📈 Performance Observation

* First packet is processed by controller (PacketIn event)
* Controller installs flow rule
* Subsequent packets are forwarded directly by switch
* This reduces latency and improves efficiency

---

## 🧠 Key Concepts

* **SDN (Software Defined Networking):** Separation of control and data planes
* **PacketIn Event:** Triggered when no flow rule matches
* **Match–Action Rule:** Defines how packets are handled
* **Learning Switch:** Dynamically learns MAC-to-port mapping

---

## 🎯 Features Implemented

* Packet capture using controller events
* Protocol identification (Ethernet, IP, TCP/UDP)
* Logging to terminal and file
* Flow rule installation
* Learning switch behavior

Test Cases

1. **Ping Test**

   * Command: `pingall`
   * Result: 0% packet loss

2. **Host-to-Host Communication**

   * Command: `h1 ping h2`
   * Result: Continuous packet flow with reduced latency

---

Conclusion

This project successfully demonstrates an SDN-based packet logging system using POX controller. It captures and analyzes network traffic, logs packet details, and improves forwarding efficiency using controller-installed flow rules.

