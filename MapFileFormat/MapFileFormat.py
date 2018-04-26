# -*- coding:utf-8 -*-
from __future__ import with_statement
import sys
import os

def map2format(in_file, out_file,options):
    with open(out_file, 'w') as fout:
        with open(in_file) as fin:
            isInSegTable = False
            isInNameTable=False
            isInProgramEntryLine=False
            nNameTable=0  #名称表头列数
            nNameTableBody=0 #名称表体解析出的列数
            seg=0x0
            segstart=0x0
            seglist=[]
            segstartlist=[]
            addr=0x0
            segTable=[]
            for line in fin:
                list = line.split()
                if len(list)==0:
                    continue
                if list[0]=="Start":
                    isInSegTable=True
                    fout.write(line)
                    continue
                if list[0]=="Address":
                    isInSegTable=False
                    isInNameTable=True
                    nNameTable=len(list)-2
                    fout.write(line)
                    continue
                if list[0]=="Program":  # "Program entry point at 0001:000445D1"
                    isInNameTable=False
                    isInProgramEntryLine=True
                    fout.write(line)
                    continue
                if isInSegTable==True:
                    temp1,temp2=list[0].split(':',1)
                    seg=int(temp1,16)
                    segstart=int(temp2,16)
                    seglist.append(seg)
                    segstartlist.append(segstart)
                    #segTable.append(seg,addr)
                    fout.write(line)
                    continue
                if isInNameTable==True:
                    nNameTableBody=len(list)
                    symbol=""
                    i=0
                    for token in list:
                    
                        i+=1
                        if nNameTableBody >nNameTable:  #表格体列数>表格头列数,说明名称列有空格等符号
                            
                            if token==list[0]:#说明是地址列
                                templist=token.split(':')
                                if len(templist)>1:                 #是相对地址
                                    start=segstartlist[int(templist[0])-1]
                                    tmpaddr=int(templist[1],16)
                                    if options.absAddr==True:   #参数选项中指定转为绝对地址
                                        addr=start + tmpaddr
                                        addrtext="{:x}".format(addr)
                                    else:
                                        addrtext=token
                                    continue
                                else:                                #是绝对地址
                                    addrtext=token
                                    continue
                            if token!=list[nNameTableBody-1]:      #不是最后一列
                                
                                
                                symbol=symbol+token+'_'
                                
                            else:                                  #是最后一列
                                
                                symbol=symbol+token
                                #fout.write(" "+list[0]+ "       "+symbol+'\n')
                        else:                  #符号名中没有空格
                        
                        
                            
                            if token==list[0]:#说明是地址列
                                templist=token.split(':')
                                if len(templist)>1:         #是相对地址
                                    start=segstartlist[int(templist[0])-1]
                                    tmpaddr=int(templist[1],16)
                                    if options.absAddr==True:               #参数选项中指定转为绝对地址
                                        start=segstartlist[int(templist[0])-1]
                                        tmpaddr=int(templist[1],16)
                                        addr=start + tmpaddr
                                        addrtext="{:x}".format(addr)
                                    else:                                  #不必强转为绝对地址.
                                        addrtext=token
                                    
                                else:                        #是绝对地址
                                    addrtext=token
                                continue
                            if token!=list[nNameTableBody-1]:    #不是最后一列
                                
                                #addrtext="{:x}".format(addr)
                                symbol=symbol+token+'_'
                                #fout.write(" "+addrtext+ "       "+symbol+'\n')
                            else:                              #是最后一列
                                #addrtext="{:x}".format(addr)
                                symbol=symbol+token
                                #fout.write(" "+list[0]+ "       "+symbol+'\n')
                    fout.write(" "+addrtext+ "       "+symbol+'\n')
def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog <map filename> [-s] [----fix_space_in_name] [-a] [--absolute_address]")
    parser.add_option("-s","--replace_space_in_name",action="store_true",dest="space",default="True",help="替换符号名中的空格") 
    parser.add_option("-a","--absolute_address",action="store_true",dest="absAddr",default="False",help="强制转为绝对地址") 
    parser.add_option("-I","--IDA_map",action="store_true",dest="IDAMap",default="False",help="IDA符号文件兼容(预留选项)") 
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error('incorrect number of arguments,please type -h for help.')
    #if options.split()
    return map2format(args[0], os.path.splitext(args[0])[0]+'_fix.map',options)

if __name__=="__main__":
    sys.exit(main())
