from scapy.all import *
from optparse import OptionParser

def get_user_input():
    parser = OptionParser()
    parser.add_option("-i", "--ip", dest="ip_range", help="Enter your IP range")
    (options, args) = parser.parse_args()
   
    if not options.ip_range:
        print("Enter your IP range \n Example: 10.100.0.1/24")
        exit()  # Programı sonlandırır
    return options.ip_range

def sending_packet(ip_range):
    arp_packet = ARP(pdst=ip_range)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = ether_frame / arp_packet

    answered_list, unanswered_list = srp(combined_packet, timeout=1,verbose=False)
    print(f"{' IP ADDRESS':<17}{' MAC ADDRESS':<20}")
    print("=" * 35)
    for cevaplanan in answered_list:

        print(" ",f"{cevaplanan[1].psrc:<17}{cevaplanan[1].src:<20}")



   

    #for cevap in answered_list:
        # Cevaplanan paketin IP ve MAC adreslerini al
      #  print("İp Address :          MAC Address ")
       # print(cevap[1].psrc,        cevap[1].hwsrc)


ip_range = get_user_input()
sending_packet(ip_range)
