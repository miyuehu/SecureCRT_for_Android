# $language = "python"
# $interface = "1.0"

#Created by miyuehu@qq.com on 2017/7/5.

#可根据盒子的实际输出做调整

#等待开机输出到串口上字符串“lowmemorykiller: oom_adj 15 => oom_score_adj 1000”,便于此时机，执行logcat命令
reboot_start_ready = "lowmemorykiller: oom_adj 15 => oom_score_adj 1000"

#捕捉开机过程中异常打印
#java.lang.NullPointerException
#android.os.DeadObjectException
#/data/anr/traces.txt
reboot_Exception_Watchdog = "Watchdog"
reboot_Exception_NullPointer= "java.lang.NullPointerException"
reboot_Exception_DeadObject = "android.os.DeadObjectException"
reboot_Exception_anr = "/data/anr/traces.txt"

#等待正常开机后的打印
reboot_start_end = "create /var/sky_stb_ChannelBackAndSmartEpg.cfg"


#logcat命令
cmd_logcat = "logcat -v time"
cmd_reboot = "reboot"

def Main():
	crt.Screen.Synchronous = True
	if not crt.Session.Connected:
                crt.Dialog.MessageBox("检查SecureCRT是否已链接")
		return
	#重启次数
	reboot_count = 0

	while True:
                #输出重启次数
                #参数True表示发送的是字符串，非命令
                crt.Screen.Send("\n重启次数reboot_count=%d\n\n"%(reboot_count), True)
                #等待重启至reboot_start_ready
                crt.Screen.WaitForString(reboot_start_ready, 30)
                #chr(3)发送‘中断键’、chr(13)发送‘enter键’，等待shell
                crt.Screen.Send(chr(3))
                crt.Screen.Send(chr(13))
                crt.Screen.WaitForString("root@Hi3798CV200:/ # ")
                #执行logcat命令
                SendCmd(cmd_logcat)
                #等待正常开机字符串标志
                #WaitForString未指定timeout时间，意味着一直等
                result = crt.Screen.WaitForString(reboot_Exception_DeadObject, 90)
                if result == 0:
                        #中断cmd_logcat命令输出，发送ctrl + c
                        crt.Sleep(2000)
                        crt.Screen.Send(chr(3))
                        crt.Screen.Send(chr(3))
                        #记录重启次数
                        reboot_count += 1
                        #执行reboot命令
                        SendCmd(cmd_reboot)
                else:
                        break
                            

def SendCmd(cmd):
	# Returns true if the text in 'send' was successfully sent and the
	# text in 'expect' was successfully found as a result.

	# If we're not connected, we can't possibly return true, or even
	# send/receive text
	if not crt.Session.Connected:
		return

        while True:
                crt.Screen.Send(cmd + chr(13))
                #避免上一个chr(13)无效，多发一次，方便快捷。
                crt.Screen.Send(chr(13))
                #此处WaitForStrings含义在于：有的时候发送到串口的字符串会异常。
                #匹配到cmd字符串，返回1
                #未匹配字符串，返回0
                #1表示等待超时1s
                result = crt.Screen.WaitForStrings(cmd, 1)
                #cmd
                if result == 1:
                        break
                #多次发送ctrl + c
                crt.Screen.Send(chr(3))
                crt.Sleep(1000)
                crt.Screen.Send(chr(3))
                
        #crt.Dialog.MessageBox(str(result))
                
	return True
            

Main()
