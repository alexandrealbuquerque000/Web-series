
#Alexandre Maia Aquino de Albuquerque

from datetime import date
import speech_recognition 
from gtts import gTTS
from playsound import playsound
import webbrowser
import pyautogui
import time
import sys
import os
import shutil
import pathlib

def presets():
    global allquestions, width, height

    width, height=pyautogui.size()

    allquestions={  'reboot':"Deseja reiniciar o programa? ",
                    'Série':"Fale a série desejada :",
                    'rep':"Deseja ativar a reprodução automática? ",
                    'typeofwatch':"Deseja escolher um episódio específico ou prefere continuar de onde parou? ",
                    'temporada':"Digite a temporada desejada: ",
                    'episódio':"Digite o episódio desejado: ",
                    'watchonemoreep':"Deseja ver mais um episódio? ",
                    'maratona':"Deseja maratonar? ",
                    'epsequence':"Digite quantos episódios seguidos deseja ver: ",
                    'timeepisodesinfo2':"Digite quantos minutos têm em cada episódio: ",
                    'rever':"Deseja recomeçar a série? ",
                    'continuarmaratona':"Deseja continuar a maratona?"  }

    pyautogui.FAILSAFE = False

    navegador=webbrowser.open("https://www.google.com/", autoraise=True)
    time.sleep(2.50)
    pyautogui.hotkey("Ctrl","K")
    time.sleep(0.25)
    pyautogui.typewrite("Por favor, apenas feche esta guia quando o programa terminar. Pode falar...esse App ficou top!")
    time.sleep(0.15)
    pyautogui.hotkey("Alt","Tab")


#Função responsável por ouvir e reconhecer a fala:
def ouvir_microfone(msg):
    while True:
     #Habilita o microfone para ouvir o usuário
        microfone = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
          #Chama a função de redução de ruido disponível na speech_recognition
            microfone.adjust_for_ambient_noise(source)
          #Avisa ao usuário que esta pronto para ouvir
            print(msg)
            if "speak" in comandvoz:
                cria_audio(msg)
            else:
                pass
          #Armazena a informação de audio na variavel
            audio = microfone.listen(source)
        try:
          #Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = microfone.recognize_google(audio,language='pt-BR')
          #Após alguns segundos, retorna a frase falada
            print()
            print("Você disse: " +frase)
            if "speak" in comandvoz:
                cria_audio("Você disse: " +frase)
            else:
                pass
            break
        #Caso nao tenha reconhecido o padrão de fala, exibe esta mensagem
        except speech_recognition.UnknownValueError:
            print()
            print("Desculpe, não entendi.")
            if "speak" in comandvoz:
                cria_audio("Desculpe, não entendi.")
            else:
                pass
            print()
            print("Tente novamente.")
            if "speak" in comandvoz:
                cria_audio("Tente novamente.")
            else:
                pass
            print()
            continue
        except speech_recognition.RequestError:
            print()
            print("Por favor, verifique sua conexão com a internet.")
            print()
            print("Tente novamente.")
            print()
            continue
            
    return frase


def audiocontfunction():
    while True:
        audiocont=audiocont+1

        yield audiocont


#Função responsável por reproduzir o que foi dito:
def cria_audio(audio):
    if audiocontnumbers==0:
        audiocontnumbers=audiocontfunction()   
    audiocont=next(audiocontnumbers)
    tts = gTTS(audio,lang="pt-br")
    #Salva o arquivo de áudio
    try:
        os.mkdir("audiopys")
    except (OSError) or (FileExistsError):
        pass
    try:
        tts.save("audiopys/audiopy"+str(audiocont)+".mp3")
    except PermissionError:
        print()
        print("Verifique se todos os arquivos 'audiopy' anteriores estão apagados.")
        print()
        input("O programa será desligado.")
        sys.exit()
    #Da play ao áudio
    playsound("audiopys/audiopy"+str(audiocont)+".mp3")
    #remove o áudio para, posteriormente, adicionar um novo
    

#Função verificadora de números decimais para comando de voz:
def leiafloatvoz(msg):
    while True:
        try:
            limiter4=float(msg.strip().replace(" ", ""))
        except (ValueError, TypeError, IndexError):
            print()
            print("ERRO:""\nDiga apenas números.")
            if "speak" in comandvoz:
                cria_audio("ERRO:""\nDiga apenas números.")
            else:
                pass
            print()
            break
        else:
            return limiter4


#Função para ouvir apenas letras:
def leiastrvoz(msg):
    while True:
        verif=str(msg.strip().replace(" ", ""))
        if verif.isalpha() == False:
            print()
            print("ERRO:""\nDiga apenas letras.")
            if "speak" in comandvoz:
                cria_audio("ERRO:""\nDiga apenas letras.")
            else:
                pass
            print()
            break
        else:
            verif=verif.lower()
            return verif
        
        
#Função verificadora de números inteiros para comando de voz:
def leiaintvoz(msg):
    while True:
        try:
            limiter4=int(msg.strip().replace(" ", ""))
        except (ValueError, TypeError, IndexError):
            print()
            print("ERRO:""\nDiga apenas números inteiros.")
            if "speak" in comandvoz:
                cria_audio("ERRO:""\nDiga apenas números inteiros.")
            else:
                pass
            print()
            break
        else:
            return limiter4
        
        
#Função para ler apenas letras:
def leiastr(msg):
    while True:
        print()
        verif=str(input(msg).strip().replace(" ", ""))
        if verif.isalpha() == False:
            print()
            print("ERRO:""\nDigite apenas letras.")
            continue
        else:
            verif=verif.lower()
            return verif


#Função desligar programa:
def desligar():
    print()
    print("Agradecemos por usar o programa! ;)")
    if "speak" in comandvoz:
        cria_audio("Agradecemos por usar o programa! ;)")
        try:
            shutil.rmtree("audiopys")
        except (OSError) or (FileNotFoundError):
            pass
    else:
        pass
    input()
    sys.exit()


#Função verificadora de existência de dados:
def verifexist(dados):
    try:
        verifexist=conteudo[(dados)]
    except (IndexError):
        erroarq()
        reboot=perguntas('reboot', 'str')
        if "s" in reboot:
            return -1
        else:
            desligar()
    else:
        return verifexist
    

#Função verificadora caso numepisodesinfo esteja com dados errados
def leiaintforQ(msg):
    try:
        limiter4=int(msg)
    except (ValueError, TypeError, IndexError):
        erroarq()
        reboot=perguntas('reboot', 'str')
        if "s" in reboot:
            return -1
        else:
            desligar()
    else:
        return limiter4
    
        
#Função para iniciar a reprodução automática:
def startrepauto():
    pyautogui.position()
    time.sleep(10+(systime/1.5))
    posxfirstclick=((width/2)+posx)*(72.5/100)
    posyfirstclick=((height/2)-posy)*(165/100)                        
    if  posxfirstclick > width:
                    posxfirstclick = width
    elif posxfirstclick < -(width):
                    posxfirstclick = -(width)
    else:
        pass
    if posyfirstclick > height:
                    posyfirstclick = height
    elif posyfirstclick < -(height):
                    posyfirstclick = -(height)
    else:
        pass
    time.sleep(0.5+systime/50)
    pyautogui.hotkey("Ctrl", "1")
    pyautogui.moveTo(width, height/2)
    time.sleep(0.5+systime/50)
    im1 = pyautogui.screenshot(region=(int((0.95-posxy)*(width/2)), int((0.95-posxy)*(height/2)), int((1.05+posxy)*(width/2)), int((1.05+posxy)*(height/2))))
    time.sleep(0.5+systime/50)
    pyautogui.hotkey("Ctrl", "2")
    time.sleep(2.5+systime/15)
    pyautogui.click((posxfirstclick), (posyfirstclick))      
    time.sleep(15+systime)
    pyautogui.middleClick(((width/2)+posx), ((height/1.5)-posy))
    for loop1 in range(2):
        time.sleep(0.5+systime/50)
        pyautogui.hotkey("Ctrl", "t")
    time.sleep(0.5+systime/50)
    pyautogui.hotkey("Ctrl", "4")
    for loop2 in range(2):
        time.sleep(0.25+systime/50)
        pyautogui.hotkey("Ctrl", "F4")
    time.sleep(0.5+systime/50)
    pyautogui.moveTo(width, height/2)
    while pyautogui.screenshot(region=(int((0.95-posxy)*(width/2)), int((0.95-posxy)*(height/2)), int((1.05+posxy)*(width/2)), int((1.05+posxy)*(height/2))))==im1:
        time.sleep(0.75+systime/45)
        pyautogui.hotkey("Ctrl", "F4")
        continue
    else:
        pass
    time.sleep(10+systime/5)
    pyautogui.click(((width/2)+posx), ((height/2.35)-posy))
    time.sleep(10+systime/5)
    pyautogui.doubleClick(((width/2)+posx), ((height/2)-posy))
    time.sleep(0.5+(systime/25))
    pyautogui.moveTo(width, height/2)
    im3=pyautogui.screenshot(region=(int((0.90-posxy)*(width/2)), int((0.945-posxy)*(height/2)), int((1.10+posxy)*(width/2)), int((1.055+posxy)*(height/2))))
    time.sleep(2.5+systime/15)
    pyautogui.moveTo(width, height/2)
    if im3==pyautogui.screenshot(region=(int((0.90-posxy)*(width/2)), int((0.945-posxy)*(height/2)), int((1.10+posxy)*(width/2)), int((1.055+posxy)*(height/2)))):
        pyautogui.press('space')
    else:
        pass
    pyautogui.press('up', presses=10)
    pyautogui.position()
    
    
#Função para abrir nova janela:
def novajanela():
    time.sleep(0.25+(systime/50))
    pyautogui.hotkey("Alt","Tab")
    time.sleep(0.5+(systime/100))
    pyautogui.hotkey("Ctrl", "n")
    
    
#Função verificadora do tempo/episódio:
def leiatemp(msg):
        while True:
            try:
                limiter4=float((msg))
            except (ValueError, TypeError, IndexError):
                erroarq()
                reboot=perguntas('reboot', 'str')
                if "s" in reboot:
                    return -1
                else:
                    desligar()
            else:
                if limiter4 < 0:
                    limiter4=limiter4*(-1)
                else:
                    pass
                return limiter4
            

#Função verificadora de números inteiros
def leiaint(msg):
    while True:
        try:
            print()
            limiter4=int(input(msg).strip().replace(" ", ""))
        except (ValueError, TypeError, IndexError):
            print()
            print("ERRO:""\nDigite apenas números inteiros.")
            continue
        else:
            return limiter4
        
        
#Função verificadora de números decimais
def leiafloat(msg):
    while True:
        try:
            print()
            limiter4=float(input(msg).strip().replace(" ", ""))
        except (ValueError, TypeError, IndexError):
            print()
            print("ERRO:""\nDigite apenas números.")
            continue
        else:
            return limiter4
            
            
#Função para fazer perguntas:
def perguntas(perg, tipo):
    perg=allquestions[perg]
    pergcopy=perg
    if tipo=='str':
        tipo1=leiastrvoz
        tipo2=leiastr
        tipo3=str
    elif tipo=='int':
        tipo1=leiaintvoz
        tipo2=leiaint
        tipo3=int
    elif tipo=='float':
        tipo1=leiafloatvoz
        tipo2=leiafloat
        tipo3=float
    else:
        tipo1=None
        tipo2=input
        tipo3=str
    if "s" in comandvoz:
        print()
        perg=ouvir_microfone(perg.replace("Digite", "Diga")).lower()
        if tipo1!=None:
            while tipo1(perg)==None:
                perg=str(pergcopy)
                perg=ouvir_microfone(perg.replace("Digite", "Diga")).lower()
            else:
                pass
        else:
            pass
    else:
        if tipo2==input:
            print()
        perg=tipo2(perg)

    if type(perg)==int or type(perg)==float:
        return tipo3(perg)
    else:
        return tipo3(perg.strip())


#Função que pede (se necessário) 'Enter' para prosseguir:
def Enter():
    if "s" in comandvoz:
        print()
        input("Pressione 'Enter' para prosseguir.")
        if "speak" in comandvoz:
            cria_audio("Pressione 'Enter' para prosseguir.")
        else:
            pass
        print()
        

def erroarq():
    print()
    print("Por favor, confira se todos os dados do arquivo estão corretos e desligue/reinicie o programa")
    if "speak" in comandvoz:
        cria_audio("Por favor, confira se todos os dados do arquivo estão corretos e desligue ou reinicie o programa")
    else:
        pass
    

def filetest():
    global conteudo
#Dados do arquivo:
    try:
        arquivo = open(str(Série)+ ".txt", 'r')                             
    except (FileNotFoundError, IndexError):
        print()
        print("Esse arquivo não existe.")
        if "speak" in comandvoz:
            cria_audio("Esse arquivo não existe.")
        else:
            pass
        reboot=perguntas('reboot', 'str')
        if "s" in reboot:
            return -1
        else:
            desligar()         
    else:
        pass
    conteudo = arquivo.readlines()


def numepisodesinfotest():
    global numepisodesinfo
    numepisodesinfo=verifexist(4)
    if numepisodesinfo==-1:
        return -1
    numepisodesinfofix=[]
    for testnumepisodes in numepisodesinfo:
        try:
            int(testnumepisodes)
        except (IndexError, ValueError):
            if '\n' in testnumepisodes:
                pass
            else:
                numepisodesinfo=numepisodesinfo.replace(testnumepisodes, ' ')
    numepisodesinfo=str(numepisodesinfo).split()


def positionstest():
    global posx, posy, posxy

    try:
        posxy=float(conteudo[6])
    except (IndexError, ValueError, TypeError):
        posxy=0
    else:
        posxy=float(posxy)
        if posxy>80:
            posxy=80
        elif posxy<-80:
            posxy=-80
        else:
            pass
#Teste das coordenadas:
    try:
        posx=str(conteudo[0].split()[:conteudo[0].split().index(',') + 1][-2])
        posy=str(conteudo[0].split()[conteudo[0].split().index(',') + 1:][0])
        float(posx)
        float(posy)
    except (ValueError, TypeError, IndexError):
        posx=0
        posy=0
    else:
        posx=float(posx)
        posy=float(posy)
        if posx > width/2:
            posx=width/2
        elif posx < -(width/2):
            posx = -(width/2)
        if posy > height/2:
            posy = height/2
        elif posy < -(height/2):
            posy = -(height/2)            
        pass


def systimetest():
    global systime
#configuração avançada (velocidade do sistema)
    try:
        systime=str(conteudo[5].split()[conteudo[5].split().index('[') + 1:][0])
        systime=float(systime)
    except (ValueError, TypeError, IndexError):
        systime=0
    else:
        if systime<0:
            systime=0
        elif systime>100:
            systime=100
        pass


def timeepisodesinfotest():
    global timeepisodesinfo1
    try:
        timeepisodesinfo1=str(conteudo[5].split()[:conteudo[5].split().index('min/ep') + 1][0])
        testeerrox=(conteudo[7].split()[:conteudo[7].split().index('x') + 1])
    except (IndexError, ValueError):
        erroarq()
        reboot=perguntas('reboot', 'str')
        if "s" in reboot:
            return -1
        else:
            desligar()
    else:
        pass


def createnumtemporadas():
    global numtemporadas

    for loop3 in numepisodesinfo:
        loop3=leiaintforQ(loop3)
        if loop3==-1:
            return -1
    numtemporadas=len(numepisodesinfo)


def arqtests():
    global URL
    URL=verifexist(1)
    if URL==-1 or numepisodesinfotest()==-1 or createnumtemporadas()==-1 or timeepisodesinfotest()==-1 or positionstest()==-1 or systimetest()==-1:
        return -1


#Guardar a data atual:
def dataday():
    data_atual=str(date.today())
    data_atual=data_atual.replace("-", " ")
    data_atual=(data_atual.split())
    data_atual=list(data_atual[::-1])
    data_atual='-'.join(map(str, data_atual))

    return data_atual
    

#Apresentando programa:
def initshow():
    os.system("cls")
    print()
    print("WebSeries Program by Alê")


def firstsconfig():  
    global limiter1, limiter2, comandvoz, Série

    limiter1="reverselimiter1"
    limiter2="x"
    comandvoz=leiastr("Deseja ativar o comando por voz? ")
    #Digite o nome da série:
    Série=perguntas('Série', None)
    if filetest()==-1 or arqtests()==-1:
        return -1


def eptemoption():
    global timeepisodesinfo1

    try:
        float(timeepisodesinfo1)
    except (ValueError, TypeError, IndexError, NameError):
        timeepisodesinfo2=perguntas('timeepisodesinfo2', 'float')    
    else:
        timeepisodesinfo2=float(timeepisodesinfo1)
    if timeepisodesinfo2<0:
        timeepisodesinfo2=timeepisodesinfo2*(-1)
    else:
        pass
    
    return timeepisodesinfo2


def closeandgoback(tmp):
    timeepisodesinfo2=tmp
    time.sleep(float(timeepisodesinfo2)*60)
    pyautogui.hotkey("Alt","F4")
    time.sleep(0.25+(systime/50))
    pyautogui.hotkey("Alt","Tab")


def especificepoption():
    global watchonemoreep, veriftest1, veriftest2
    temporada=0
    while temporada==0:
        veriftest1=0
        temporada=perguntas('temporada', 'int')             
        for loop4 in list(range(1, numtemporadas+1)) :
            while True:
                if int(temporada)==loop4:
                    veriftest2=numepisodesinfo[veriftest1]           
                    break
                else:
                    veriftest1=veriftest1+1
                    break
        else:
            if int(temporada) not in range(numtemporadas+1):
                temporada=0
                print()
                print("Essa temporada não existe")
                if "speak" in comandvoz:
                    cria_audio("Essa temporada não existe")
                else:
                    pass
                print()
                print("Essa série tem",numtemporadas,"temporadas")
                if "speak" in comandvoz:
                    cria_audio("Essa série tem{}temporadas".format(numtemporadas))
                else:
                    pass
        temporada=int(temporada)
        while temporada!=0:
            print()
            print("Essa temporada possui",veriftest2,"episódios")
            if "speak" in comandvoz:
                cria_audio("Essa temporada possui{}episódios".format(veriftest2))
            else:
                pass
            episódio=perguntas('episódio', 'int')
            if episódio in range(int(veriftest2)+1) and episódio!=0:
                formatedurl=str(URL).format(temporada, episódio)
                if 's' in rep:
                    timeepisodesinfo2=eptemoption()
                novajanela()
                navegador=webbrowser.open(formatedurl, autoraise=True)
                if "s" in rep:
                    startrepauto()
                else:
                    pass
                break
            else:
                print()
                print("Esse episódio não existe")
                if "speak" in comandvoz:
                    cria_audio("Esse episódio não existe")
                else:
                    pass
                continue
        else:
            continue
    else:
        if "s" in rep:
            closeandgoback(timeepisodesinfo2)
        else:
            pass
        Enter()
        watchonemoreep=perguntas('watchonemoreep', 'str')         
        if "s" in watchonemoreep and "s" in rep:
            novajanela()
            time.sleep(0.5+(systime/25))
            pyautogui.hotkey("Ctrl", "Alt", "Tab");pyautogui.press("right");pyautogui.press("right");pyautogui.press("enter")
        else:
            pass
        

def continuepreviewepoption():
    global limiter4, limiter6, continuarmaratona, epsequence

    if limiter3=="limiter3":
        maratona="x"
        limiter7=1
    else:
        limiter7=0
        maratona=perguntas('maratona', 'str') 
    if "s" in maratona or "s" in continuarmaratona and limiter6!="limiter6":
        limiter1="limiter1"
        limiter4=1
        epsequence=perguntas('epsequence', 'int')    
        if epsequence < 0:
            epsequence=-(epsequence)
        elif epsequence==0:
            epsequence=1
        else:
            pass
    else :
        if limiter7==1:
            pass
        else:
            limiter4=1
            epsequence=1
            pass    
    limiter5=0
    veriftest1=0
    arquivo = open(str(Série)+ ".txt", 'r')
    conteudo = arquivo.readlines()
    for loop5 in range(numtemporadas+1):
        if str(loop5) in (conteudo[7].split()[:conteudo[7].split().index('x') + 1]):
            temporada = 0 + int(loop5)
            limiter5=1
            if temporada==0:
                temporada=1
            else:
                pass
            for loop6 in list(range(1, numtemporadas+1)) :
                while not int(temporada)==loop6:
                    veriftest1=veriftest1+1
                    break
                else:
                    veriftest2=numepisodesinfo[veriftest1]
                    break
    if temporada not in range(1,numtemporadas+1) and limiter5!=1:
        erroarq()
        reboot=perguntas('reboot', 'str')
        if "s" in reboot:
            return -1
        else:
            desligar() 
    for loop7 in range(int(veriftest2)+1):
        limiter5=0
        if str(loop7) in (conteudo[7].split()[conteudo[7].split().index('x') + 1:]):
            episódio = 0 + int(loop7)
            limiter5=1
            break
    else:
        try:
            limiter4=int(episódio)
        except (ValueError, TypeError, IndexError, NameError):
            erroarq()
            reboot=perguntas('reboot', 'str')
            if "s" in reboot:
                return -1
            else:
                desligar()  
        else:
            pass
        
        if  episódio not in range(1,int(veriftest2)+1) and episódio==0 and limiter5!=1:
            erroarq()
            reboot=perguntas('reboot', 'str')
            if "s" in reboot:
                return -1
            else:
                desligar()  
    arquivo.close()
    if 's' in rep or 's' in maratona:
        timeepisodesinfo2=eptemoption()
    formatedurl=str(URL).format(temporada, episódio+1)
    episódio=episódio+1
    novajanela()
    navegador=webbrowser.open(formatedurl, autoraise=True)
    if "s" in rep:
        startrepauto()
    else:
        pass

    def endofseries(): 
        nonlocal episódio, temporada

        if episódio==int(numepisodesinfo[temporada-1]):
            temporada=temporada+1
            episódio=0
    #mostrando que a séria acabou se temporada for maior que o número de temporadas
            if temporada>numtemporadas:
                aux2=[]
                aux3=[]
                print()
                print("A série acabou")
                if "speak" in comandvoz:
                    cria_audio("A série acabou")
                else:
                    pass
                Enter()
                rever=perguntas('rever', 'str')           
                arquivo = open(str(Série)+ ".txt", 'r')
                conteudo=arquivo.readlines()
                arquivo.seek(0)
                if "s" in rever:
                    temporada=1
                    try:
                        conteudo[9]
                    except (IndexError):        
                        pass
                    else:
                        arquivo = open(str(Série)+ ".txt", 'r')
                        conteudo = arquivo.readlines()
                        arquivo.close()
                        for aux5 in conteudo:
                            if aux5!=conteudo[9]:
                                arquivo = open(str(Série)+ ".txt", 'w')
                                aux2.append(aux5)
                                arquivo.writelines(aux2)
                        arquivo.truncate()
                        arquivo.close()
                        pass
                    arquivo = open(str(Série)+ ".txt", 'r')
                    conteudo=arquivo.readlines()
                    for aux6 in conteudo:  
                        if aux6 != conteudo[7]:
                            arquivo.close()
                            arquivo = open(str(Série)+ ".txt", 'w')
                            aux3.append(aux6)
                            arquivo.writelines(aux3)
                        else:
                            break
                    arquivo.truncate()
                    arquivo.close()
                    arquivo = open(str(Série)+ ".txt", 'r')
                    conteudo=arquivo.readlines()
                    conteudo.append("Último episódio visto: 0 x 0 .".rstrip('\n\n\n'))
                    arquivo = open(str(Série)+ ".txt", 'w')
                    arquivo.writelines(conteudo)
                    arquivo.truncate()
                    arquivo.close()
                    pass
                else:
                    try:
                        conteudo[9]
                    except (IndexError) :
                        conteudo.append("\n\nA série terminou.")
                        arquivo = open(str(Série)+ ".txt", 'w')
                        arquivo.writelines(conteudo)
                        arquivo.truncate()
                        arquivo.close()
                        pass
                    else:
                        if '\n' in conteudo[9]:
                            conteudo.append("A série terminou.")
                            arquivo = open(str(Série)+ ".txt", 'w')
                            arquivo.writelines(conteudo)
                            arquivo.truncate()
                            arquivo.close()
                            pass
                        else:
                            pass
                    reboot=perguntas('reboot', 'str')
                    if "s" in reboot:
                        return -1
                    else:
                        desligar()

        return episódio, temporada

    episódio, temporada=endofseries()

    def refreshtxtfileinfo():
        nonlocal episódio, temporada

        arquivo = open(str(Série)+ ".txt", 'r')
        conteudo=arquivo.readlines()
        arquivo.seek(0)
        aux1=[]
        for aux4 in conteudo:
            if aux4 != conteudo[7]:
                arquivo.close()
                arquivo = open(str(Série)+ ".txt", 'w')
                aux1.append(aux4)
                arquivo.writelines(aux1)
        arquivo.truncate()
        arquivo.close()
        arquivo = open(str(Série)+ ".txt", 'r')
        conteudo=arquivo.readlines()
        conteudo.append("Último episódio visto: {} x {} . ({}) ".format( temporada , episódio, dataday()).rstrip('\n\n'))
        arquivo = open(str(Série)+ ".txt", 'w')
        arquivo.writelines(conteudo)
        arquivo.truncate()
        arquivo.close()


    def maratonacontroler():
        global limiter2, limiter3, limiter4, limiter6, continuarmaratona, watchonemoreep
        nonlocal maratona, timeepisodesinfo2

        while limiter4%epsequence !=0:
            limiter4=limiter4+1
            time.sleep(timeepisodesinfo2*60)
            pyautogui.hotkey("Alt","F4")
            novajanela()
            limiter3="limiter3"
            limiter6="limiter6"
            limiter2="limiter2"
            break
        else:
            while "s" in maratona or limiter2=="limiter2":
                if "s" in rep:
                    closeandgoback(timeepisodesinfo2)
                else:
                    pass            
                Enter()
                continuarmaratona=perguntas('continuarmaratona', 'str')
                if "s" in continuarmaratona:
                    if "s" in rep:
                        novajanela()
                        time.sleep(0.5+(systime/25))
                        pyautogui.hotkey("Ctrl", "Alt", "Tab");pyautogui.press("right");pyautogui.press("right");pyautogui.press("enter")        
                        pass
                    else:
                        pass
                    limiter3="limiter3"
                    maratona="s"
                    limiter6="continuarmaratona"
                    limiter2="limiter2"
                    break
                else:
                    limiter2="x"
                    maratona="maratona"
                    pass
            else:
                if "maratona"==maratona:
                    watchonemoreep="continuarmaratona"
                    pass
                else:
                    if "s" in rep:
                        closeandgoback(timeepisodesinfo2)
                    else:
                        pass
                    Enter()
                    watchonemoreep=perguntas('watchonemoreep', 'str')  
                    if "s" in watchonemoreep and "s" in rep:
                        novajanela()
                        time.sleep(0.5+(systime/25))
                        pyautogui.hotkey("Ctrl", "Alt", "Tab");pyautogui.press("right");pyautogui.press("right");pyautogui.press("enter")                     
                    else:
                        pass   

    refreshtxtfileinfo()
    maratonacontroler()


def secondsconfig():
    global rep, limiter3, limiter6, continuarmaratona, watchonemoreep

    if firstsconfig()==-1:
        return -1
    reboot='n'
    print()
    print("Série:__",Série,"__")
    if "speak" in comandvoz:
            cria_audio("Série: {}".format(Série))
    else:
        pass
    rep=perguntas('rep', 'str')
    watchonemoreep="s"
    limiter3="x"
    limiter6='x'
    continuarmaratona="continuarmaratona"
    while "s" in watchonemoreep:
        if "limiter3" in limiter3:
                pass
        else:
            typeofwatch=perguntas('typeofwatch', 'str')     
        if "ep" in typeofwatch:
            especificepoption()
        else:
            if continuepreviewepoption()==-1:
                return -1
            else:
                pass
    else:
        if "s" not in reboot:
            reboot=perguntas('reboot', 'str')
            if "s" in reboot:
                return -1
            else:
                desligar()


def run():
    presets()
    #Mecanismo para reiniciar programa:
    reboot="s"
    while "s" in reboot:
        initshow()
        if secondsconfig()==-1:
            continue


run()



    
   


        

    
