from Preprocessing import *
import matplotlib.pyplot as plt
dir = 'C:/Users/user/switchdrive/Wristband Comparison/Signals/'

######## E4 ###########################################################
# Read the raw file and create a file in the directory related to te session (e.g session 1 , 2 ,..) only with Time and EDA
for i in range(1,10):

 file_e4 = dir + 'E4/' + str(i) + '/EDA.csv'
 eda = signal_extraction(file_e4,'empatica','EDA')
 eda_db = time_extraction(eda,'EDA')
 eda_db.to_csv(dir + 'E4/' +str(i) + '/EDA_Time.csv',index = 0)
 time = eda_db['Time'].values
 plt.figure()
 plt.ylabel('EDA')
 plt.title('E4' + ' ' + 'Session' + ' ' + str(i))
 plt.plot(eda_db['EDA'])
 plt.savefig(dir + 'E4/' + str(i) + '/EDA.png')
 print ("Folder %s beg %s end %s " % (i, time[0],time[len(time)-1]))

#Create a file with beginning and end of each sesssion
e4_timestamp_beg = pandas.to_datetime(['2017-08-28 16:25:45.00', '2017-08-28 23:08:39.00','2017-08-29 06:50:09.00', '2017-08-29 22:11:09.00',
                 '2017-08-30 06:41:19.00','2017-08-30 22:42:23.00','2017-08-31 22:56:39.00','2017-09-01 06:47:31.00',
                 '2017-09-02 09:24:37.00']).values
e4_timestamp_end = pandas.to_datetime(['2017-08-28 20:59:55.00', '2017-08-29 06:14:20.50','2017-08-29 19:02:10.00','2017-08-30 06:13:19.00',
                 '2017-08-30 19:40:50.00','2017-08-31 21:19:46.50','2017-09-01 06:14:16.00','2017-09-01 19:42:38.00',
                 '2017-09-02 21:56:09.50']).values
df = pandas.DataFrame({'Beginning':e4_timestamp_beg,'End':e4_timestamp_end})
df.to_csv(dir + 'E4/Time_sessions.csv',index=0)



################### Biovotion ##################################################################################
#Open the file with all the session and create n (n = number of sessions) file with EDA and Time in each folder
file_biovision = dir + 'Biovotion/raw.csv'
eda = signal_extraction(file_biovision,'biovotion','EDA')
eda.to_csv(dir + 'Biovotion/EDA_Time.csv',index = 0)
plt.plot(eda['EDA'])

# Timestamp of the sessions - Beginning
bio_timestamp_beg = pandas.to_datetime(['2017-08-28 15:57:23 ', '2017-08-28 22:52:19', '2017-08-29 06:47:37',
'2017-08-29 22:08:09', '2017-08-30 06:41:13', '2017-08-30 22:39:47', '2017-08-31 22:55:35', '2017-09-01 06:46:27',
'2017-09-02 09:23:27']).values
# Timestamp of the sessions - End
bio_timestamp_end = pandas.to_datetime(['2017-08-28 21:04:01' ,'2017-08-29 06:13:55', '2017-08-29 19:02:34' ,'2017-08-30 06:13:35',
'2017-08-30 19:40:20', '2017-08-31 21:04:25','2017-09-01 06:13:58', '2017-09-01 19:42:23', '2017-09-02 20:59:45']).values
# File with the session
df = pandas.DataFrame({'Beginning':bio_timestamp_beg,'End':bio_timestamp_end})
df.to_csv(dir + 'Biovotion/Time_sessions.csv',index=0)

# Divide the raw file in sessions according to the timestamp
for i in range(1, len(bio_timestamp_end)+1):
    eda_part = part_div(eda['EDA'],eda['Time'],bio_timestamp_beg[i-1],bio_timestamp_end[i-1])
    time_part = part_div(eda['Time'],eda['Time'],bio_timestamp_beg[i-1],bio_timestamp_end[i-1])
    db = pandas.DataFrame({'EDA':eda_part,'Time':time_part})
    db.to_csv(dir + 'Biovotion/' +str(i) + '/EDA_Time.csv',index = 0)
    plt.figure()
    plt.title('Biovotion' + ' ' + 'Session' + ' ' + str(i))
    plt.ylabel('EDA')
    plt.plot(eda_part)
    plt.savefig(dir + 'Biovotion/' +str(i) + '/EDA.png')
    print i


############### Comparison ##############################################################################################

shift = (e4_timestamp_beg - bio_timestamp_beg)/np.timedelta64(1,'s')
print ("The time difference for the beginning of each session is %s " % (shift))

shift_end = (e4_timestamp_end - bio_timestamp_end)/np.timedelta64(1,'s')
print ("The time difference for the end of each session is %s " % (shift_end))
