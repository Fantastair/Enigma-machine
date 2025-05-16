import tkinter as tk
import machine
from machine import batch_o, rotor_group, keyboard

def converse(string, mode = 1):
	# 十进制和十六进制的互换
	#
	# 默认为十进制转十六进制
	# 输入和输出都是字符串

	if mode:
		return hex(int(string))[2:].upper()
	else:
		return int(int(string, 16))

batch_x = converse(batch_o)
rotate_state = 0

def rotate(site, anchor = 1):
	# 这将根据指定位置和方向拨动一次转子
	global rotate_state

	rotate_state += 26 ** site * anchor
	rotate_state = rotate_state % 26 ** len(rotor_group)
	parse(rotate_state)
	show()

def parse(total):
	# 这将同步转子的转动状态与总状态一致

	for rotor in rotor_group[::-1]:
		rotor.rotate_state = total // 26 ** rotor.num
		total -= 26 ** rotor.num * rotor.rotate_state

def show():
	# 这将显示转子当前的转动状态到tk图形界面上

	for rotor in rotor_group:
		state[rotor.num].set(rotor.rotate_state)

def encrypt():
	# 这将转换输入框中的字符并显示到输出框

	origin_string = text_in.get('0.0', tk.END)[:-1]
	string = ''
	for s in origin_string:
		if ord(s.lower()) > 122 or ord(s.lower()) < 97:
			string += s
		else:
			captial = s.isupper()
			if captial:
				string += keyboard.in_put(s.lower()).upper()
			else:
				string += keyboard.in_put(s)
			rotate(0)

	text_out.delete('0.0', tk.END)
	text_out.insert('0.0', string)

# Tk窗口
root = tk.Tk()
root.configure(bg = 'black')
root.title('恩格玛机 1.3')

# 框架
control_frame = tk.Frame(root, bg = 'black')
control_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
show_frame = tk.Frame(root, bg = 'black')
show_frame.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)

# 显示程序版本和批次
tk.Label(root, text = '恩格玛机 1.3\n批次:'+batch_x, bg = 'black', fg = 'lime',
	font = ('幼圆',20)).grid(row = 0, column = 0)

# 转轮控制台
state = []
for s in range(3):
	number = tk.StringVar()
	number.set(0)
	state.append(number)

	tk.Button(control_frame, text = '↑', bg = 'black',
		fg = 'lime', font = ('幼圆',20),
		command = lambda site = s:rotate(site),
		).grid(row = 0, column = 2-s, padx = 10, pady = 5)
	tk.Label(control_frame, textvariable = state[s], bg = 'black',
		fg = 'lime', font = ('幼圆',20),
		).grid(row = 1, column = 2-s, padx = 10, pady = 5)
	tk.Button(control_frame, text = '↓', bg = 'black',
		fg = 'lime', font = ('幼圆',20),
		command = lambda site = s:rotate(site, -1),
		).grid(row = 2, column = 2-s, padx = 10, pady = 5)

# 输入框和输出框
text_in = tk.Text(show_frame, bg = 'dimgray', fg = 'navy',
	font = ('黑体',20), height = 9, width = 30)
text_in.pack(side = tk.LEFT, padx = 10, pady = 10)
tk.Button(show_frame, text = '=>\n\n转\n换\n\n=>', bg = 'black',
		fg = 'lime', font = ('幼圆',20), command = encrypt,
		).pack(side = tk.LEFT, pady = 10)
text_out = tk.Text(show_frame, bg = 'dimgray', fg = 'navy',
	font = ('黑体',20), height = 9, width = 30)
text_out.pack(side = tk.LEFT, padx = 10, pady = 10)

root.mainloop()

