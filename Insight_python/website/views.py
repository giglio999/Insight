from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from bs4 import BeautifulSoup
import requests
import re

views = Blueprint('views', __name__)

class ReclameAqui:
    def __init__(self,empresa):

        self.empresa = str(empresa)
        self.url = f"https://www.reclameaqui.com.br/empresa/{empresa}/"
        print(self.url)

        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

        self.page = requests.get(self.url, headers=self.headers)

        self.soup = BeautifulSoup(self.page.text, features = "html.parser")

        self.dados = self.soup.find("div", class_ = "go267425901" ).text.replace(" ","")

        self.data = re.findall("\d+\.\d+|\d+|[-]+", self.dados)

        self.dataset = []

        self.totalComplains = []
        self.answeredPercentual = []
        self.totalNotAnswered = []
        self.totalEvaluated = []
        self.consumerScore = []
        self.dealAgainPercentual = []
        self.solvedPercentual = []
        self.averageAnswerTime = []
        
        '''for i in range(9):
            
            if self.data[i].isnumeric():
                self.dataset.append(self.data[i])
            else:
                self.dataset.append("Não possui dados suficientes")'''

    def getData(self):

        self.dados = self.soup.find("script", {"id": "__NEXT_DATA__"} ).text.replace(" ","")
        self.tab = re.findall('(?:^|\W)consumerScore(?:$|\W)+\d*.\d*|(?:^|\W)consumerScore(?:$|\W)+\d+', self.dados)
        self.tab1 = re.findall('(?:^|\W)solvedPercentual(?:$|\W)+\d*.\d*|(?:^|\W)solvedPercentual(?:$|\W)+\d+', self.dados)
        self.tab2 = re.findall('(?:^|\W)averageAnswerTime(?:$|\W)+\d*.\d*|(?:^|\W)averageAnswerTime(?:$|\W)+\d+', self.dados)
        self.tab3 = re.findall('(?:^|\W)totalEvaluated(?:$|\W)+\d*.\d*|(?:^|\W)totalEvaluated(?:$|\W)+\d+', self.dados)
        self.tab4 = re.findall('(?:^|\W)totalNotAnswered(?:$|\W)+\d*.\d*|(?:^|\W)totalNotAnswered(?:$|\W)+\d+', self.dados)
        self.tab5 = re.findall('(?:^|\W)answeredPercentual(?:$|\W)+\d*.\d*|(?:^|\W)answeredPercentual(?:$|\W)+\d+', self.dados)
        self.tab6 = re.findall('(?:^|\W)dealAgainPercentual(?:$|\W)+\d*.\d*|(?:^|\W)dealAgainPercentual(?:$|\W)+\d+', self.dados)
        self.tab7 = re.findall('(?:^|\W)totalComplains(?:$|\W)+\d*.\d*|(?:^|\W)totalComplains(?:$|\W)+\d+', self.dados)
        

        for i in range(len(self.tab7)):
            self.temp = re.findall("\d+|[--]+", self.tab7[i])
            if i >= 6 and i <= 10:
                self.totalComplains.append(self.temp[0].replace("--","0"))

        for i in range(len(self.tab5)):
            self.temp1 = re.findall("\d+\.\d+|[--]+", self.tab5[i])
            if i >= 6 and i <= 10:
                self.answeredPercentual.append(self.temp1[0].replace("--","0"))

        for i in range(len(self.tab4)):
            self.temp2 = re.findall("\d+|[--]+", self.tab4[i])
            if i >= 6 and i <= 10:
                self.totalNotAnswered.append(self.temp2[0].replace("--","0"))

        for i in range(len(self.tab3)):
            self.temp3 = re.findall("\d+|[--]+", self.tab3[i])
            if i >= 6 and i <= 10:
                self.totalEvaluated.append(self.temp3[0].replace("--","0"))

        for i in range(len(self.tab)):
            self.temp4 = re.findall("\d+\.\d+|[--]+", self.tab[i])
            if i >= 6 and i <= 10:
                self.consumerScore.append(self.temp4[0].replace("--","0"))

        for i in range(len(self.tab6)):
            self.temp5 = re.findall("\d+\.\d+|[--]+", self.tab6[i])
            if i >= 6 and i <= 10:
                self.dealAgainPercentual.append(self.temp5[0].replace("--","0"))

        for i in range(len(self.tab1)):
            self.temp6 = re.findall("\d+\.\d+|[--]+", self.tab1[i])
            if i >= 6 and i <= 10:
                self.solvedPercentual.append(self.temp6[0].replace("--","0"))

        for i in range(len(self.tab2)):
            self.temp7 = re.findall("\d+\.\d+|[--]+", self.tab2[i])
            if i >= 6 and i <= 10:
                self.averageAnswerTime.append(float(self.temp7[0])/86400)

        self.dataset.append(self.totalComplains)
        self.dataset.append(self.answeredPercentual)
        self.dataset.append(self.totalNotAnswered)
        self.dataset.append(self.totalEvaluated)
        self.dataset.append(self.consumerScore)
        self.dataset.append(self.dealAgainPercentual)
        self.dataset.append(self.solvedPercentual)
        self.dataset.append(self.averageAnswerTime)

    def displayData(self):
        print(f" Reclamações recebidas: {self.dataset[0]} \n Reclamações respondidas: {self.dataset[1]}% \n Reclamações a responder: {self.dataset[2]} \n Reclamações avaliadas: {self.dataset[3]} \n Nota média dos avaliadores: {self.dataset[4]} \n Voltariam a fazer negócio: {self.dataset[5]} % \n Recçamaçoes resolvidas : {self.dataset[6]}% \n Tempo médio para respostas: {self.dataset[7]} dias e {self.dataset[8]} horas")


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    '''if request.method == 'POST':    
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note id too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')'''

    if not current_user.company :
        empresa = str("ReclameAqui").replace(" ", "-").lower()
    else:
        empresa = str(current_user.company).replace(" ", "-").lower()

    reclame = ReclameAqui(empresa)
    reclame.getData()

    recebidas6 = reclame.dataset[0][0]
    recebidas12 = reclame.dataset[0][1]
    recebidas2023 = reclame.dataset[0][2]
    recebidas2022 = reclame.dataset[0][3]
    recebidas_geral = reclame.dataset[0][4]

    respondidas6 = reclame.dataset[1][0]
    respondidas12 = reclame.dataset[1][1]
    respondidas2023 = reclame.dataset[1][2]
    respondidas2022 = reclame.dataset[1][3]
    respondidas_geral = reclame.dataset[1][4]
    
    agurdando6 = reclame.dataset[2][0]
    agurdando12 = reclame.dataset[2][1]
    agurdando2023 = reclame.dataset[2][2]
    agurdando2022 = reclame.dataset[2][3]
    agurdando_geral = reclame.dataset[2][4]

    avaliada6 = reclame.dataset[3][0]
    avaliada12 = reclame.dataset[3][1]
    avaliada2023 = reclame.dataset[3][2]
    avaliada2022 = reclame.dataset[3][3]
    avaliada_geral = reclame.dataset[3][4]

    media6 = reclame.dataset[4][0]
    media12 = reclame.dataset[4][1]
    media2023 = reclame.dataset[4][2]
    media2022 = reclame.dataset[4][3]
    media_geral = reclame.dataset[4][4]

    voltariam6 = reclame.dataset[5][0]
    voltariam12 = reclame.dataset[5][1]
    voltariam2023 = reclame.dataset[5][2]
    voltariam2022 = reclame.dataset[5][3]
    voltariam_geral = reclame.dataset[5][4]

    tempo6 = reclame.dataset[6][0]
    tempo12 = reclame.dataset[6][1]
    tempo2023 = reclame.dataset[6][2]
    tempo2022 = reclame.dataset[6][3]
    tempo_geral = reclame.dataset[6][4]


    return render_template("home.html", user=current_user,
    recebidas6 = recebidas6, recebidas12 = recebidas12, recebidas2023 = recebidas2023, recebidas2022 = recebidas2022, recebidas_geral = recebidas_geral,
    respondidas_geral = respondidas_geral, respondidas2022 = respondidas2022, respondidas2023 = respondidas2023, respondidas12 = respondidas12, respondidas6 = respondidas6,
    agurdando6 = agurdando6, agurdando12 = agurdando12, agurdando2023 = agurdando2023, agurdando2022 = agurdando2022, agurdando_geral = agurdando_geral,
    avaliada6 = avaliada6, avaliada12 = avaliada12, avaliada2023 = avaliada2023, avaliada2022 = avaliada2022, avaliada_geral = avaliada_geral,
    media6 = media6, media12 = media12, media2023 = media2023, media2022 = media2022, media_geral = media_geral,
    voltariam6 = voltariam6, voltariam12 = voltariam12, voltariam2023 = voltariam2023, voltariam2022 = voltariam2022, voltariam_geral = voltariam_geral,
    tempo6 = tempo6, tempo12 = tempo12, tempo2023 = tempo2023, tempo2022 = tempo2022, tempo_geral = tempo_geral)