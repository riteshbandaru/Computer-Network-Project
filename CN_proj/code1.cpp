#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/log.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("TcpRenoExample");

int main (int argc, char *argv[])
{
  // Enable logging
  LogComponentEnable ("TcpRenoExample", LOG_LEVEL_INFO);
  LogComponentEnable ("TcpReno", LOG_LEVEL_ALL);

  // Set up default parameters
  uint32_t payloadSize = 1024; // Size of the data in the TCP packet (bytes)
  uint32_t segmentSize = 512;  // Size of the TCP segment (bytes)
  double simulationTime = 10.0; // Time for the simulation (seconds)

  CommandLine cmd;
  cmd.AddValue ("payloadSize", "Size of data in the packet", payloadSize);
  cmd.AddValue ("segmentSize", "Size of TCP segment", segmentSize);
  cmd.AddValue ("simulationTime", "Simulation Time in seconds", simulationTime);
  cmd.Parse (argc, argv);

  // Create nodes
  NodeContainer nodes;
  nodes.Create (2);

  // Set up point-to-point link
  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  // Install devices on the nodes
  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

  // Install Internet stack with TCP Reno
  InternetStackHelper internet;
  internet.Install (nodes);

  // Set up IP addresses
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = ipv4.Assign (devices);

  // Create an OnOff application (generates traffic)
  OnOffHelper onoff ("ns3::TcpReno", Address (InetSocketAddress (interfaces.GetAddress (1), 9))); // Sending to node 1, port 9
  onoff.SetConstantRate (DataRate ("1Mbps"));
  onoff.SetAttribute ("PacketSize", UintegerValue (payloadSize));
  ApplicationContainer apps = onoff.Install (nodes.Get (0)); // Install on node 0 (sender)
  apps.Start (Seconds (1.0)); // Start sending at 1s
  apps.Stop (Seconds (simulationTime)); // Stop sending after simulationTime

  // Create a packet sink application (receives the traffic)
  PacketSinkHelper sink ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), 9)); // Listen on port 9
  apps = sink.Install (nodes.Get (1)); // Install on node 1 (receiver)
  apps.Start (Seconds (0.0));
  apps.Stop (Seconds (simulationTime));

  // Enable pcap tracing
  pointToPoint.EnablePcapAll ("tcp-reno-simulation");

  // Run the simulation
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}