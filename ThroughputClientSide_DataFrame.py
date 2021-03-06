# this code extract the RTT for each stream of TCP flows in multiple pcap files
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import time
import pandas as pd

if __name__=="__main__":
    transmission_time=17
    col=["blue", "green" , "red"]
    cc=["Reno","Cubic","BBR"]
    col_iter=0



  # pcaps located on my external hard disks


    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/mobile/MobileTotal/bbr',]

    paths = ['/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/reno',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/cubic',
             '/Volumes/Untitled/log-mobile_20180124/rmbt/498/stationary/StationaryTotal/bbr',]





    for path in paths:
       df_result = pd.DataFrame(columns=['group', 'rtt', 'thr'])
       counter=0
       ave_throughput = []
       ave_rtt=[]
       rtt_total = []
       pcap_files = [pos_pcap for pos_pcap in os.listdir(path) if pos_pcap.endswith('.pcap')]
       for index, pcap_file in enumerate(pcap_files):
           #print("started")
           #print(pcap_file)
           p=os.path.join(path, pcap_file)
           print(pcap_file)

           #tshark command for stationary2 pcaps
           #command = "tshark -r " + p + " -2  -R  '(ip.src == 46.194.205.245) && (ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > ./tmp/"+pcap_file+".csv"
           command = "tshark -r " + p + " -2  -R  '(ip.dst == 130.243.27.222) && (tcp.stream>=0)' -T fields -e tcp.stream -e frame.time_relative -e tcp.seq -E separator=, > "+p+".csv"
           command_rtt = "tshark -r " + p + " -2  -R  '(ip.src == 130.243.27.222) && (tcp.stream>=0) && (tcp.analysis.ack_rtt>0)' -T fields -e tcp.stream -e tcp.analysis.ack_rtt -E separator=, > "+p+"RTT.csv"


           try:
               #print("I am running the command")
               df = pd.read_csv(p + ".csv", names=['stream', 'time', 'seq'])
               df_rtt = pd.read_csv(p + "RTT.csv", names=['stream', 'rtt'])

           except:
               os.system(command)
               os.system(command_rtt)
               df = pd.read_csv(p + ".csv", names=['stream', 'time', 'seq'])
               df_rtt = pd.read_csv(p + "RTT.csv", names=['stream', 'rtt'])




           for level in pd.unique(df.iloc[:,0]):
               #print(pd.unique(df.iloc[:,0]))
               df_s = df.loc[df.stream == level]
               df_rtt_level = df_rtt.loc[df_rtt.stream == level]


               df_2=df_s.sub(df_s.iloc[0,1], axis=1)

               df_tmp = df_2.sort_index(ascending=False)  # reverse the data frame to get the last row

               #ave_throughput.append(df_tmp.iloc[0,2]/1000000/(df_tmp.iloc[0,1]-8))
               ave_throughput.append(df_tmp.iloc[0, 2] / 1000000 / transmission_time)
               ave_rtt.append(df_rtt_level['rtt'].mean())




       plt.figure(1)
       plt.plot(ave_throughput , ave_rtt, 'o', markersize=3, color=col[col_iter], label=cc[col_iter])
       plt.legend()
       plt.ylabel('Ave. RTT [sec]')
       plt.xlabel('Ave. Throughput [Mbps]')
       plt.xlim(0, 4)
       plt.ylim(0, 4)
       #df_res[col_iter].to_csv(p + "_rtt_throuput"+cc[col_iter]+".csv", index=False, header=False)
       col_iter = col_iter + 1
       df_result=pd.DataFrame([np.array(ave_throughput), np.array(ave_rtt)]).T
       df_result.to_csv(path+"Average_rtt_thr.csv", index = False, header = False)
       ave_throughput=[]
       ave_rtt=[]
       del(df_result)
    plt.show()


