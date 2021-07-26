from tkinter import *
from collections import deque
import numpy as np
from pyfinite import ffield

counter = 0
ERROR=0
look = 0
look_for_first = 0 

hex_and_binary = True
root = Tk()
width=1000
height=700
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.title("AES_Encryption")



Mix_column_matrix= [[2 , 3 , 1 ,1],
                    [1 , 2 , 3 , 1],
                    [1 , 1 , 2 , 3],
                    [3, 1 , 1 , 2]]


def xor(a, b): 
    ans = "" 
    for i in range(len(a)): 
        if a[i] == b[i]: 
            ans = ans + "0"
        else: 
            ans = ans + "1"
    return ans 


sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
        ]
        
      

#Key_Generator###############################################################################
def AES_Encrypt(Plain_text , KEY):
    global ERROR
    global hex_and_binary
    if len(Plain_text)>32 or len(Plain_text)<32 or len(KEY)>32 or len(KEY)<32:
        Error_label['text'] = 'Make sure the plain text and the key have the right length'
        ERROR = 1
        plain_text_entry['bg'] = 'red'
        key_entry['bg'] = 'red'
        raise ValueError("Make sure the plain text and the key have the right length")
    elif len(Plain_text)==32 and len(KEY)==32:
        ERROR = 0 
        Error_label['text'] = ' '   
        
    global counter
    def key_generator(key , rc):
        #Convert hex to binary#############################################
        round0 = "{0:08b}".format(int(key, 16)).zfill(128)
        print('Hello' , round0)
        #Key_rounds########################################################
        key_array = []
        for i in range(0 , 127 , 32):
            key_array.append(round0[i : i+32])
        
        #next_round########################################################
        key_next_round = []
        W3 = deque([])
        #Function_g########################################################

        for i in range(0 , 31 , 8):
            W3.append(key_array[3][ i : i+8])
        
         
        W3.rotate(-1) 
        
        #S-Boxes###########################################################
        SUB = []
        for i in W3:
            x = int(i[0:4],2)
            y = int(i[4:8],2)
            SUB.append(sbox[x][y])
            
         

        for i in range(0 ,4):
            SUB[i] = bin(SUB[i])[2:].zfill(8)

        y = str(SUB[0]) 
        
        
        gFunOutput = []
        RC_array=['00000001' , '00000010' , '00000100' , '00001000' , '00010000' , '00100000' , '01000000' , '10000000' , '00011011' , '00110110']
        RC = xor(RC_array[rc] , y)
        
        gFunOutput.append(RC)
        gFunOutput.append(SUB[1])
        gFunOutput.append(SUB[2])
        gFunOutput.append(SUB[3])


        

        All_in_gFunction= gFunOutput[0]+gFunOutput[1]+gFunOutput[2]+gFunOutput[3]
        
        
        word3_g_function_With_word0 = xor(str(All_in_gFunction) , str('{0:b}'.format(int(key_array[0],2))).zfill(32)).zfill(32)
        word1_word0_output = xor(word3_g_function_With_word0 ,str('{0:b}'.format(int(key_array[1],2)).zfill(32)).zfill(32))
        word2_word1_output = xor(word1_word0_output , str('{0:b}'.format(int(key_array[2],2)).zfill(32) ).zfill(32))
        word3_word2_output = xor(word2_word1_output , str('{0:b}'.format(int(key_array[3],2)).zfill(32)).zfill(32) )


        key_next_round.append(word3_g_function_With_word0)
        key_next_round.append(word1_word0_output)
        key_next_round.append(word2_word1_output)
        key_next_round.append(word3_word2_output)
        
        


        k_round = key_next_round[0]+key_next_round[1]+key_next_round[2]+key_next_round[3]
       
    
        decimal = int(k_round , 2)
        
        
        key_round1INhex = hex(decimal).lstrip('0x').zfill(32)
        
        return key_round1INhex , k_round  
        #end of key Generator######################################################

        
    all_key_rounds=[]
    all_key_rounds_in_binary=[]
    #keys = 'f1eaa6f70b94f27a0b7231b0b06d8fa6'
    keys = KEY
    
    all_key_rounds.append(keys)
    all_key_rounds_in_binary.append("{0:08b}".format(int(keys, 16)).zfill(128))
    for i in range(0 , 10):
        
        keys , keys_in_bin = key_generator(keys , i)
        all_key_rounds.append(keys)
        all_key_rounds_in_binary.append(keys_in_bin)
    print('Keys ',all_key_rounds , len(all_key_rounds))
    print(all_key_rounds_in_binary , len(all_key_rounds_in_binary))    





    #AES########################################################################################################
    #Converting Plain text from hex to binary ##################################################
    #pt ='153817f5e3b4f6fec117998c15d3aad1'
    pt = Plain_text
    pt_b = "{0:08b}".format(int(pt, 16)).zfill(128)
    #xor plain text with k0 ####################################################################
    pt_after_xor_in_binary = xor(pt_b , "{0:08b}".format(int(all_key_rounds[0], 16)).zfill(128))
    
    decimal1 = int(pt_after_xor_in_binary , 2)
    pt_after_xor_in_hex = hex(decimal1).lstrip('0x').zfill(32)   
    

    #S-Boxes#############################################################################
    def SBoxess(pt_after_xor_in_binary):
        pt_A_array = []
        for i in range(0 , 127 , 8):
            pt_A_array.append(pt_after_xor_in_binary[i:i+8]) 
            

        B_array=[]
        for i in pt_A_array:
            x=int(i[0:4],2)
            y=int(i[4:8],2)
            
            B_array.append(sbox[x][y])
        
        Out_put =''
        out_put_in_hexa=''
        for i in B_array:
            Out_put+= bin(i).lstrip('0b').zfill(8)
            out_put_in_hexa += hex(i).lstrip('0x').zfill(2) 

        print("         " , Out_put , len(Out_put))
        B_array_2D = np.reshape(B_array , (4, 4) , 'F')
        
        return B_array_2D , Out_put , out_put_in_hexa


    #Shift_rows#########################################################################
    def Shift_Rows(B_array_2D):
        B_shift_rows= []
        for i in range(0 , 4):
            B_array_shift= deque(B_array_2D[i])
            B_array_shift.rotate(-i)
            B_shift_rows.append(B_array_shift)
        B_shift_rows = np.reshape(B_shift_rows , (4 , 4))    
        
        One_column_1 = np.reshape(B_shift_rows[:,0] , (4,1))
        One_column_2 = np.reshape(B_shift_rows[:,1] , (4,1))
        One_column_3 = np.reshape(B_shift_rows[:,2] , (4,1))
        One_column_4 = np.reshape(B_shift_rows[:,3] , (4,1))
        
        finallll=''
        finallll_in_hex=''
        
        for i in range(4):
            for j in range(4):
                finallll += bin(B_shift_rows[j][i]).lstrip('0b').zfill(8)
                finallll_in_hex += hex(B_shift_rows[j][i]).lstrip('0x').zfill(2) 
        return B_shift_rows , finallll , finallll_in_hex



    #Mix_Column################################################################################
    def MixColumnn(B_shift_rows ):
        f = ffield.FField(8 , gen=0x11b , useLUT=0)
        
        C_column=[[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]

        for i in range(len(Mix_column_matrix)):
            
            for j in range(len(B_shift_rows[0])):
                
                for k in range(len(B_shift_rows)):
                    C_column[i][j] = f.Add(f.Multiply(Mix_column_matrix[i][k] , B_shift_rows[k][j]) , C_column[i][j])
                    
       
        print(C_column[0][0])
        final_result_before_xor_hexa = '' 

        for i in range(0 , 4):
            for i in range (0 , 4):
                final_result_before_xor_hexa += hex(C_column[j][i]).lstrip('0x').zfill(2)   
        for i in range(0 , 4):
            
            for j in range(0 , 4):
                
                C_column[i][j] = bin(C_column[i][j]).lstrip('0b').zfill(8)
                

        
        final_result_before_xor = ''
        
        for i in range(4):
            for j in range(4):
                final_result_before_xor += C_column[j][i]
                

        print('final' , final_result_before_xor , len(final_result_before_xor))
        return final_result_before_xor , final_result_before_xor_hexa


        #Key_addition#################################################################################
    def Key_additionnn(final_result_before_xor , rounds): 
        FINAL_RESULT = xor(final_result_before_xor , all_key_rounds_in_binary[rounds])
        FINAL_RESULT_IN_DECIMAL = int(FINAL_RESULT , 2)
        FINAL_RESULT_IN_HEX = hex(FINAL_RESULT_IN_DECIMAL).lstrip('0x').zfill(32)
        
        return FINAL_RESULT , FINAL_RESULT_IN_HEX


    No_Operation = 'No Operation'
    outPut_of_Sboxes = []
    outPut_of_shiftRows = [] 
    outPut_of_mixColumn = [] 
    outPut_of_Sboxes.append(No_Operation)
    outPut_of_shiftRows.append(No_Operation)
    outPut_of_mixColumn.append(No_Operation)
    outPut_of_Sboxes_hexa = []
    outPut_of_shiftRows_hexa = [] 
    outPut_of_mixColumn_hexa = [] 
    outPut_of_Sboxes_hexa.append(No_Operation)
    outPut_of_shiftRows_hexa.append(No_Operation)
    outPut_of_mixColumn_hexa.append(No_Operation) 
    All_result_in_pt = []
    All_result_in_pt_hex = []
    pt_test = pt_after_xor_in_binary
    pt_test_in_hex = pt_after_xor_in_hex
    All_result_in_pt.append(pt_test)
    All_result_in_pt_hex.append(pt_test_in_hex)
    for i in range(1,11):
        if i != 10:
            s_boxes_output1 , s_boxes_output2 , s_boxes_output3 = SBoxess(pt_test)
            outPut_of_Sboxes.append(s_boxes_output2)
            outPut_of_Sboxes_hexa.append(s_boxes_output3)
            pt_test , eshta , eshta_in_hex = Shift_Rows(s_boxes_output1)
            outPut_of_shiftRows.append(eshta)
            outPut_of_shiftRows_hexa.append(eshta_in_hex)
            outOf_mixColumn , outOf_mixColumn_hexa  = MixColumnn(pt_test)
            outPut_of_mixColumn.append(outOf_mixColumn)
            outPut_of_mixColumn_hexa.append(outOf_mixColumn_hexa)
            pt_test , pt_test_in_hex = Key_additionnn(outOf_mixColumn, i)
            All_result_in_pt.append(pt_test)
            All_result_in_pt_hex.append(pt_test_in_hex)
            
        else :
            s_boxes_output1 , s_boxes_output2 , s_boxes_output3 = SBoxess(pt_test)
            outPut_of_Sboxes.append(s_boxes_output2)
            outPut_of_Sboxes_hexa.append(s_boxes_output3)
            x , y  , y_hex= Shift_Rows(s_boxes_output1)
            outPut_of_shiftRows.append(y)
            outPut_of_shiftRows_hexa.append(y_hex)
            pt_test , pt_test_in_hex = Key_additionnn(y , i)
            All_result_in_pt.append(pt_test)
            All_result_in_pt_hex.append(pt_test_in_hex)
    outPut_of_mixColumn.append(No_Operation)
    outPut_of_mixColumn_hexa.append(No_Operation)      
    

    #Gui_Control####################
    if hex_and_binary is True:
        Error_label['text'] = ''
        Sub_byte_output['text'] = outPut_of_Sboxes[counter]
        Shift_rows_output['text'] = outPut_of_shiftRows[counter]
        Mix_column_output['text'] = outPut_of_mixColumn[counter]
        Key_in_binary_output['text'] = all_key_rounds_in_binary[counter]
        Key_Addition_output['text'] = All_result_in_pt[counter]
        Rounds_counter['text'] = 'R' + str(counter)
        Plain_text_Bin_output['text'] = pt_b
        plain_text_entry['bg'] = '#ffffff'
        key_entry['bg'] = '#ffffff'
        plain_text_entry['state'] = 'disabled'
        key_entry['state'] = 'disabled'
        ERROR = 0
    else:
        Error_label['text'] = ''
        Sub_byte_output['text'] = outPut_of_Sboxes_hexa[counter]
        Shift_rows_output['text'] = outPut_of_shiftRows_hexa[counter]
        Mix_column_output['text'] = outPut_of_mixColumn_hexa[counter]
        Key_in_binary_output['text'] = all_key_rounds[counter]
        Key_Addition_output['text'] = All_result_in_pt_hex[counter]
        Rounds_counter['text'] = 'R' + str(counter)
        Plain_text_Bin_output['text'] = pt_b
        plain_text_entry['bg'] = '#ffffff'
        key_entry['bg'] = '#ffffff'
        plain_text_entry['state'] = 'disabled'
        key_entry['state'] = 'disabled'
        ERROR = 0

        
    
    
    print(counter)

    return All_result_in_pt_hex        



def last_round():
    global counter
    counter = 10
    AES_Encrypt(plain_text_entry.get() , key_entry.get())
    Key_in_binary_output['bg'] = '#96e31b'
    Key_Addition_output['bg'] = '#96e31b'
    plain_text_entry['state'] = 'normal'
    key_entry['state'] = 'normal'
     
    return None

def first_round():
    global counter
    global look_for_first
    counter = 0
    AES_Encrypt(plain_text_entry.get() , key_entry.get())
    look_for_first = 1
    counter = 1 
    if counter == 10:
        Key_in_binary_output['bg'] = '#96e31b'
        Key_Addition_output['bg'] = '#96e31b'
        plain_text_entry['state'] = 'normal'
        key_entry['state'] = 'normal'
        
    else:
        Key_in_binary_output['bg'] = '#ffffff'
        Key_Addition_output['bg'] = '#ffffff'
    
     
    return None    
#Gui########################################################################################
First_plain_text_label = Label(root , text = 'Plain text').place(x=220,y=20,width=86,height=30)

First_key_label = Label(root , text = 'key').place(x=230,y=60,width=76,height=30)

plain_text_entry = Entry(root , text = 'Enter 128-bit plain text in hex')
plain_text_entry.place(x=340,y=20,width=300,height=30)

key_entry = Entry(root , text = 'Enter 128-bit Key in hex')
key_entry.place(x=340,y=60,width=300,height=30)
def previous_round():
    global counter
    global look
    global look_for_first
    look = 0 
    counter-=1
    AES_Encrypt(plain_text_entry.get() , key_entry.get())
    
    
    if counter ==0:
        look_for_first = 1
        counter =1
    
    if counter == 10:
        Key_in_binary_output['bg'] = '#96e31b'
        Key_Addition_output['bg'] = '#96e31b'
        plain_text_entry['state'] = 'normal'
        key_entry['state'] = 'normal'
        
    else:
        Key_in_binary_output['bg'] = '#ffffff'
        Key_Addition_output['bg'] = '#ffffff'
        
    
            
    return None

def next_round():
    global counter
    global look 
    look = 1
    AES_Encrypt(plain_text_entry.get() , key_entry.get())
    counter+=1
    if counter == 11:
        Key_in_binary_output['bg'] = '#96e31b'
        Key_Addition_output['bg'] = '#96e31b'
        plain_text_entry['state'] = 'normal'
        key_entry['state'] = 'normal'
        counter = 10 
        
    else:
        Key_in_binary_output['bg'] = '#ffffff'
        Key_Addition_output['bg'] = '#ffffff'
      
    return None

def switch():
    global hex_and_binary 
    global look 
    global counter
    global look_for_first
    hex_and_binary = not hex_and_binary
    if counter == 1 and look_for_first == 1 :
        counter -=1
        AES_Encrypt(plain_text_entry.get() , key_entry.get())
        counter +=1
        return None
    if look == 1 and counter != 10 :
        counter -=1
    look = 0
    look_for_first = 0
    AES_Encrypt(plain_text_entry.get() , key_entry.get())
    if counter == 10:
        Key_in_binary_output['bg'] = '#96e31b'
        Key_Addition_output['bg'] = '#96e31b'
        plain_text_entry['state'] = 'normal'
        key_entry['state'] = 'normal'
        
        
    else:
        Key_in_binary_output['bg'] = '#ffffff'
        Key_Addition_output['bg'] = '#ffffff'
    return None    



Encrypt_button = Button(root , text = 'Next round-->' , fg = 'blue', command=next_round).place(x=830,y=640,width=110,height=25)
Encrypt_All_button = Button(root , text = 'Last round' ,fg = 'blue', command=last_round).place(x=80,y=640,width=70,height=25)
First_Round_button = Button(root , text = 'First round' ,fg = 'blue', command=first_round).place(x=440,y=640,width=70,height=25)
Encrypt_button = Button(root , text = '<--Previous round' ,fg = 'blue', command=previous_round).place(x=720,y=640,width=110,height=25)
Switch_button = Button(root , text = 'HEX/BIN' ,fg = 'blue', command=switch).place(x=70,y=40,width=70,height=25)


Plain_text_Bin_label = Label(root , text="Plain text in binary" )
Plain_text_Bin_label.place(x=410,y=130,width=150,height=35)

Plain_text_Bin_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge")
Plain_text_Bin_output.place(x=0,y=160,width=1000,height=30)

Sub_byte_label = Label(root , text="Sub_byte" )
Sub_byte_label.place(x=410,y=200,width=150,height=35)

Sub_byte_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge")
Sub_byte_output.place(x=0,y=230,width=1000,height=30)

Shift_rows_label = Label(root , text = "Shift Rows")
Shift_rows_label.place(x=410,y=270,width=150,height=25)

Shift_rows_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge" )
Shift_rows_output.place(x=0,y=300,width=1000,height=30)

Mix_column_label = Label(root , text = "Mix Column")
Mix_column_label.place(x=410,y=340,width=150,height=25)

Mix_column_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge" )
Mix_column_output.place(x=0,y=370,width=1000,height=30)

Key_in_binary_label = Label(root , text = "Key of round")
Key_in_binary_label.place(x=410,y=410,width=150,height=25)

Key_in_binary_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge" )
Key_in_binary_output.place(x=0,y=440,width=1000,height=30)

Key_Addition_label = Label(root , text = "Key Addition (Cipher text)")
Key_Addition_label.place(x=410,y=480,width=170,height=25)

Key_Addition_output = Label(root , bg='white' ,borderwidth='3px' , relief="ridge" )
Key_Addition_output.place(x=0,y=510,width=1000,height=30)

Error_label = Label(root , fg = "red")
Error_label.place(x=660,y=40,width=330,height=36)

Rounds_counter = Label(root ,text = "R", bg='white' ,borderwidth='3px' , relief="ridge" , fg = "red" , font=("Courier", 25))
Rounds_counter.place(x=425,y=545,width=100,height=90)



root.mainloop()