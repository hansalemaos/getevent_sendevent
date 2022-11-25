# Sending touch/swipe events to BlueStacks/Android sounds easy but actually it isn't 


### There are some "common ways"

##### 1st way:

The standard version on a not rooted system is:
**adb shell input tap x y**
Unfortunately, this method is very slow and unreliable since it calls the Java layer of the android framework:
[https://stackoverflow.com/a/38806872/15096247]()

##### 2nd way:

If your cell phone / BlueStacks instance is rooted, you can use: 
**adb shell sendevent /dev/input/event2 3 0 x**
**adb shell sendevent /dev/input/event2 3 1 y**
**adb shell sendevent /dev/input/event2 1 330 1**
**adb shell sendevent /dev/input/event2 0 0 0**
**adb shell sendevent /dev/input/event2 1 330 0**
**adb shell sendevent /dev/input/event2 0 0 0**

This method is a lot better than "input tap" since it is more reliable and slightly faster.
But when you use "sendevent" like in the example above, you won't even get a decent swipe, because
the break between the ADB shell calls just takes too long. 

Even using: 
**adb shell "sendevent1 ; sendevent2 ; sendevent3 ; …"**
doesn’t improve the executing speed much.

##### 3rd way:

If your cell phone / BlueStacks instance is rooted, you can also use: 

**adb shell dd bs=filesize_in_bytes  if=./file of=/dev/input/eventX**

This method is very reliable and very very very fast… unfortunately too fast for the Android touch screen. 

## sendevent-getevent aims to offer a solution for the execution speed problem.

### Features: 


- You can record getevents directly from python, once you are done you press the hotkey (default=“ctrl+x”) to exit the recording session. 
- It converts the output into all possible formats: hex - int - sendevent with int - binary data and returns a Pandas DataFrame
- You can define the playback speed of the recorded session (speed 4 is about close to the "original speed")
- You can change the playback speed afterwards
- It is possible to save/load recorded sessions
- You can manually change the DataFrame
- It sends chunked data to the device/emulator using adb shell dd bs=filesize_in_bytes  if=./file of=/dev/input/eventX , and sleeps after each chunk


### Tested against Windows 10 / Python 3.9.13 / BlueStacks 5

It should also work with any rooted Android device, the only problem might be the "bluestacks_divider".
[https://stackoverflow.com/a/73733261/15096247]()

But changing the code (if necessary) shouldn't be a big thing. 
Since my cell phone is not rooted, and I have no intention of rooting it, I cannot test it with an physical Android device. (I would be grateful for any feedback)

Take a look at the video to see what the code below does:
[![YT](https://github.com/hansalemaos/screenshots/raw/main/bluestacksauto.png)](https://www.youtube.com/watch?v=BNDtruH6frI)
[https://www.youtube.com/watch?v=BNDtruH6frI]()
```python
$pip install getevent-sendevent

from getevent_sendevent import GetEventSendEvent
import pandas as pd

# creating an instance 
getsend = GetEventSendEvent(
    adb_path="C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
    deviceserial="localhost:5735",
    sdcard="/storage/emulated/0/",  # it is probably better to pass the path, not the symlink
    temfolder_on_sd_card="AUTOMAT", # if the folder doesn't exist, it will be created
    bluestacks_divider=32767,
    exit_keys="ctrl+x", # stop the recording session
)

# connect to adb
getsend.connect_to_adb()

# start a recording session 
df = getsend.record_events_and_convert_to_df(playbackspeed=3)

# execute the recorded command
getsend.execute_recorded_events(
    df,
    structfolder="struct",
    additional_end_command=True,
    remove_temp_files_from_device=False,
)

# increasing the execution speed
df_fast=pd.DataFrame()
for speed_ in range(4,16):
    df_fast = getsend.change_playback_speed(df, playback_speed=speed_)
    getsend.execute_recorded_events(
        df_fast,
        structfolder="struct",
        additional_end_command=True,
        remove_temp_files_from_device=False, # Repeated execution will be faster, but you should clean the folder /storage/emulated/0/AUTOMAT every once in a while
    )


# executing the same command over and over again without creating a new DataFrame
for speed_ in range(4,16):
    getsend.execute_recorded_events(
        df_fast,
        structfolder="struct", # binary data
        additional_end_command=True,
        remove_temp_files_from_device=False,
    )


# Saving the recorded session 
getsend.save_recorded_data_on_hdd(df, path="f:\\testfoldersendevent\\saveddata.txt")

# Loading it again and redefine the playback speed
dfloaded = getsend.load_recoded_data(
    path="f:\\testfoldersendevent\\saveddata.txt", playback_speed=16
)

# Executing the loaded session
getsend.execute_recorded_events(
    dfloaded,
    structfolder="struct",
    additional_end_command=True,
    remove_temp_files_from_device=False,
)

Here is the DataFrame:

     aa_time  aa_device aa_type    aa_code  aa_value aa_device_name  aa_value_int aa_code_int aa_type_int  aa_time_difference_start  aa_time_diff_actions  aa_real_coords aa_send_event aa_send_event_real_ccords  aa_time_new  aa_struct aa_struct_real  aa_struct_size  aa_struct_real_size aa_struct_together aa_struct_real_together struct_tmp_hdd_full_path struct_tmp_hdd struct_tmp_folder struct_filename struct_real_tmp_hdd_full_path struct_real_tmp_hdd struct_real_tmp_folder struct_real_filename struct_copy_dv struct_real_copy_dv  random_sleep aa_copy_struct_to_hdd aa_copy_struct_real_to_hdd struct_folder_android struct_real_folder_android struct_file_android struct_real_file_android aa_copy_struct_to_hdd_success
0  30922....  /dev/i...  EV_ABS  ABS_MT...  0000769f  BlueSt...          30367            53           3         0.0                       0.0                   889       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352            b'\x01...          b'\x03...               C:\Use...                C:\Use...      tmpcgn...         struct...       C:\Use...                     C:\Use...           tmpqeh...              struct...            dd bs=...      dd bs=...                 0.0     __main...             __main...                  /stora...             /stora...                  /stora...           /stora...                     True                   
1  30922....  /dev/i...  EV_ABS  ABS_MT...  00005974  BlueSt...          22900            54           3         0.0                       0.0                   377       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352                 <NA>               <NA>               C:\Use...                     <NA>      tmpcgn...              None       C:\Use...                          <NA>           tmpqeh...                   None                 <NA>           <NA>                 0.0           NaN                   NaN                  /stora...             /stora...                        NaN                 NaN                      NaN                   
2  30922....  /dev/i...  EV_SYN  SYN_MT...  00000000  BlueSt...              0             2           0         0.0                       0.0                     0       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352                 <NA>               <NA>               C:\Use...                     <NA>      tmpcgn...              None       C:\Use...                          <NA>           tmpqeh...                   None                 <NA>           <NA>                 0.0           NaN                   NaN                  /stora...             /stora...                        NaN                 NaN                      NaN                   
3  30922....  /dev/i...  EV_SYN  SYN_RE...  00000000  BlueSt...              0             0           0         0.0                  0.012315                     0       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352                 <NA>               <NA>               C:\Use...                     <NA>      tmpcgn...              None       C:\Use...                          <NA>           tmpqeh...                   None                 <NA>           <NA>            0.012315           NaN                   NaN                  /stora...             /stora...                        NaN                 NaN                      NaN                   
4  30922....  /dev/i...  EV_ABS  ABS_MT...  0000769f  BlueSt...          30367            53           3    0.012315                       0.0                   889       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352                 <NA>               <NA>               C:\Use...                     <NA>      tmpcgn...              None       C:\Use...                          <NA>           tmpqeh...                   None                 <NA>           <NA>                 0.0           NaN                   NaN                  /stora...             /stora...                        NaN                 NaN                      NaN                   
5  30922....  /dev/i...  EV_ABS  ABS_MT...  00005974  BlueSt...          22900            54           3    0.012315                       0.0                   377       sendev...     sendev...                         1    b'\x01...  b'\x03...            352             352                 <NA>               <NA>               C:\Use...                     <NA>      tmpcgn...              None       C:\Use...                          <NA>           tmpqeh...                   None                 <NA>           <NA>                 0.0           NaN                   NaN                  /stora...             /stora...                        NaN                 NaN                      NaN                   
....
```
