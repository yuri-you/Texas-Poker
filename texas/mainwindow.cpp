#include "mainwindow.h"
#include "ui_mainwindow.h"
//#include<iostream>

#define Play_Minimal_Size 1
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    initial();
    initial_tcp();
}
void MainWindow::initial_tcp(){
    socket=new QTcpSocket();
    connect(socket,&QTcpSocket::readyRead,this,&MainWindow::read);
    tcpisconnect=false;

    //ip and porter
    QIntValidator *port_valid=new QIntValidator(0,65535);
    ui->port->setValidator(port_valid);
    ui->ip->setText(QString("39.108.192.128"));
    ui->port->setText(QString("11000"));

    //editline
    QRegExp regExp("[^,.]+");//避免与分隔符','冲突
    ui->name->setValidator(new QRegExpValidator(regExp,this));
    ui->name->setMaxLength(10);

    //debug
    connect(ui->write_buffer,&QPushButton::clicked,this,&MainWindow::write_buffer_debug);

    //ui->player_information
    ui->player_information->clear();
    ui->player_information->addItem(QString("尚未加入房间!"));

    //connect tcp
    connect(ui->jiarufangjian,&QPushButton::clicked,this,&MainWindow::tcp_connect);
    connect(ui->tuichufangjia,&QPushButton::clicked,this,&MainWindow::tcp_disconnect);

    //ready
    connect(ui->zhunbei,&QPushButton::clicked,this,&MainWindow::ready);
    connect(ui->quxiaozhunbei,&QPushButton::clicked,this,&MainWindow::cancel_ready);

}
void MainWindow::change_name(){
    if(selfname==ui->name->text())return;
    if(tcpisconnect){
        write_buffer(QString("Change Name,%1").arg(ui->name->text()));
        int isready=players[selfname];
        players.remove(selfname);
        players.insert(ui->name->text(),isready);
        modify_user();
    }
    selfname=ui->name->text();
//    qDebug()<<selfname;
}
void MainWindow::ready(){
    if(ui->zhunbei->text()=="准备"){//非房主
        if(!tcpisconnect){
            QMessageBox::warning(this,"WARNING!","请先加入房间",QMessageBox::Yes);
            return;
        }
        if(players[ui->name->text()]==1)return;
        write_buffer("Ready,"+ui->name->text());
        players[ui->name->text()]=1;
        modify_user();
    }
    else{//房主
        if(!tcpisconnect){
            QMessageBox::warning(this,"WARNING!","请先加入房间",QMessageBox::Yes);
            return;
        }
        write_buffer("Begin Game");
    }
    ui->name->setEnabled(false);
}
void MainWindow::cancel_ready(){
    if(players[ui->name->text()]==0)return;
    write_buffer("Cancel Ready,"+ui->name->text());
    players[ui->name->text()]=0;
    modify_user();
    ui->name->setEnabled(true);
}
void MainWindow::write_buffer_debug(){
    if(!tcpisconnect){
        QMessageBox::warning(this,"WARNING!","请先联网!",QMessageBox::Yes);
        return;
    }
    socket->write(ui->buffer->text().toUtf8());
}
void MainWindow::write_buffer(QString x){
    if(!tcpisconnect){
        QMessageBox::warning(this,"WARNING!","请先加入房间",QMessageBox::Yes);
        return;
    }
    x+=".";
    socket->write(x.toUtf8());
}
void MainWindow::tcp_connect(){
    if(ui->name->text().isEmpty()){
        QMessageBox::warning(this,"WARNING!","请先输入昵称!",QMessageBox::Yes);
        return;
    }
    QString ip=ui->ip->text();
    quint16 port=ui->port->text().toUInt();
    if(socket->isValid()){
        socket->disconnectFromHost();
    }
    socket->connectToHost(ip,port);
}
void MainWindow::tcp_disconnect(){
    if(socket->isValid()){
        socket->disconnectFromHost();
        players.clear();
        modify_user();
        tcpisconnect=false;
        ui->zhunbei->setText("准备");
        ui->quxiaozhunbei->setHidden(false);
    }
}
void MainWindow::modify_user(){
    int maxsize=25;
    ui->player_information->clear();
    if(players.isEmpty()){
        ui->player_information->addItem(QString("尚未加入房间!"));

    }
    int count=1;
    for(QString t:players.keys()){
        if(t==ui->name->text()){
        QString is_ready("未准备");
        if(players[t]==1){
            is_ready="已准备";
        }
        else if(players[t]==2){
            is_ready="房主";
        }
        QString name1=QString("玩家%1(我):%2").arg(count).arg(t);
        name1+=QString(maxsize-name1.size(),' ');
        ui->player_information->addItem(QString("%1 %2").arg(name1).arg(is_ready));
        count+=1;
        break;
        }
    }
    for(QString t:players.keys()){
        if(t!=ui->name->text()){
        QString is_ready("未准备");
        if(players[t]==1){
            is_ready="已准备";
        }
        else if(players[t]==2){
            is_ready="房主";
        }
        QString name1=QString("玩家%1:%2").arg(count).arg(t);
        name1+=QString(maxsize-name1.size(),' ');
        ui->player_information->addItem(QString("%1 %2").arg(name1).arg(is_ready));
        count+=1;
        }
    }
}
void MainWindow::change_host(){
    ui->zhunbei->setText("开始游戏");
    ui->quxiaozhunbei->setHidden(true);
    ui->zhunbei->setEnabled(false);
    modify_user();
}
void MainWindow::read(){
    QByteArray buffer=socket->readAll();
    QString data = decoder->toUnicode(buffer);
    qDebug()<<"Get Information:"+data;
    QStringList datas=data.split('.');
    for(QString t:datas){
        readAll(t);
    }
}
void MainWindow::readAll(QString data){
    QStringList datas=data.split(',');
    qDebug()<<data;
    if(datas[0]=="Connect Successfully"){
        tcpisconnect=true;
        QMessageBox::information(this,"Information!","成功加入房间",QMessageBox::Yes);
        write_buffer(ui->name->text());
    }
    else if(datas[0]=="Name Repeat"){
        QMessageBox::warning(this,"WARNING!","昵称重复\n请换个昵称再重新连接",QMessageBox::Yes);
        socket->disconnectFromHost();
    }
    else if(datas[0]=="User Add"){
        players.insert(datas[1],0);
        modify_user();
    }
    else if(datas[0]=="User Leave"){
        players.remove(datas[1]);
        modify_user();
    }
    else if(datas[0]=="Ready"){
        players[datas[1]]=1;
        modify_user();
    }
    else if(datas[0]=="Cancel Ready"){
        players[datas[1]]=0;
        modify_user();
    }
    else if(datas[0]=="Initial Player Host"){
        players.insert(ui->name->text(),2);
        change_host();
    }
    else if(datas[0]=="Change Host"){
        players[datas[1]]=2;
        if(datas[1]==selfname){
            change_host();
        }
    }
    else if(datas[0]=="All Ready"){
        if(players[selfname]!=2){
            QMessageBox::warning(this,"WARNING!","出错",QMessageBox::Yes);
            exit(-1);
        }
        if(players.size()>=Play_Minimal_Size){
        ui->zhunbei->setEnabled(true);
        }
    }
    else if(datas[0]=="Not All Ready"){
        if(players[selfname]!=2){
            QMessageBox::warning(this,"WARNING!","出错",QMessageBox::Yes);
            exit(-1);
        }
        ui->zhunbei->setEnabled(false);
    }
    else if(datas[0]=="Initial Player"){
//        modify_user();
        players[datas[1]]=datas[2].toInt();
    }
    else if(datas[0]=="Initial Finish"){
        players.insert(ui->name->text(),0);
        modify_user();
    }
    else if(datas[0]=="Change Name"){
        bool isready=players[datas[1]];
        players.remove(datas[1]);
        players.insert(datas[2],isready);
        modify_user();
    }
    else Receive_Game_Instruction(datas);
//    write_buffer("Accept");
}
void MainWindow::closeEvent(QCloseEvent *e){
    socket->disconnectFromHost();
}
void MainWindow::initial(){
    decoder = QTextCodec::codecForName("UTF8");
    players.clear();
    initial_cards();
    initial_lineedit();
    ui->xiazhujine->setSingleStep(10);
    ui->fasongxiaoxi->setEnabled(false);
    ui->shoujianren->setEnabled(false);
    ui->fasongneirong->setEnabled(false);
    ui->qingkongxiaoxi->setEnabled(false);
}
void MainWindow::initial_cards(){
    ui->own_card1->setPixmap(QPixmap("poker//behind.jpg"));
    ui->own_card2->setPixmap(QPixmap("poker//behind.jpg"));
    ui->card1->setPixmap(QPixmap("poker//behind.jpg"));
    ui->card2->setPixmap(QPixmap("poker//behind.jpg"));
    ui->card3->setPixmap(QPixmap("poker//behind.jpg"));
    ui->card4->setPixmap(QPixmap("poker//behind.jpg"));
    ui->card5->setPixmap(QPixmap("poker//behind.jpg"));
}
void MainWindow::initial_lineedit(){
    //disable lineedit data
    ui->money->setEnabled(false);
    ui->youxiweizhi->setEnabled(false);
    ui->youxiweizhi->setEnabled(false);
    ui->youxiweizhi->setEnabled(false);
    ui->youxiweizhi->setEnabled(false);
    ui->youxiweizhi->setEnabled(false);

    connect(ui->name,&QLineEdit::editingFinished,this,&MainWindow::change_name);
}
MainWindow::~MainWindow()
{
    delete ui;
}

