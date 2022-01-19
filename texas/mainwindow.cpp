#include "mainwindow.h"
#include "ui_mainwindow.h"
#include<iostream>
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    initial();
    initial_tcp();
}
//void MainWindow::debug(){
//    write_buffer(QString("Yuri"));
//    socket->disconnectFromHost();
//}
void MainWindow::initial(){
    decoder = QTextCodec::codecForName("UTF8");
    QPixmap pixmap("poker//joker.jpg");
    QPixmap pixmap1("poker//AS.jpg");
    ui->own_card1->setPixmap(pixmap);
    ui->own_card2->setPixmap(pixmap);
    ui->card1->setPixmap(pixmap1);
    ui->card2->setPixmap(pixmap1);
    ui->card3->setPixmap(pixmap1);
    ui->card4->setPixmap(pixmap1);
    ui->card5->setPixmap(pixmap1);
    ui->xiazhujine->setSingleStep(10);
}
void MainWindow::initial_tcp(){
    socket=new QTcpSocket();
    connect(ui->jiarufangjian,&QPushButton::clicked,this,&MainWindow::tcp_connect);
    connect(ui->tuichufangjia,&QPushButton::clicked,this,&MainWindow::tcp_disconnect);
    connect(socket,&QTcpSocket::readyRead,this,&MainWindow::readAll);
    tcpisconnect=false;
    QIntValidator *port_valid=new QIntValidator(0,65535);
    ui->port->setValidator(port_valid);
    ui->ip->setText(QString("39.108.192.128"));
    ui->port->setText(QString("11000"));
    //debug
    connect(ui->write_buffer,&QPushButton::clicked,this,&MainWindow::write_buffer_debug);
}
void MainWindow::write_buffer_debug(){
    if(!tcpisconnect){
        QMessageBox::warning(this,"WARNING!","Please Connect the Internet First!",QMessageBox::Yes);
        return;
    }
    socket->write(ui->buffer->text().toUtf8());
}
void MainWindow::write_buffer(QString x){
    if(!tcpisconnect){
        QMessageBox::warning(this,"WARNING!","Please Connect the Internet First!",QMessageBox::Yes);
        return;
    }

    socket->write(x.toUtf8());
}
void MainWindow::tcp_connect(){
    if(ui->name->text().isEmpty()){
               QMessageBox::warning(this,"WARNING!","请先输入昵称!",QMessageBox::Yes);
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
    }
}
void MainWindow::readAll(){
    QByteArray buffer=socket->readAll();
    QString str = decoder->toUnicode(buffer);
    qDebug()<<str;
    if(str=="Connect Successfully"){
        tcpisconnect=true;
        ui->player->addItem(QString("成功加入房间"));
        write_buffer(QString("Name,")+ui->name->text());
    }
    if(str=="Name Repeat"){
        QMessageBox::warning(this,"WARNING!","昵称重复\n请换个昵称再重新连接",QMessageBox::Yes);
        socket->disconnectFromHost();
    }
}
void MainWindow::closeEvent(QCloseEvent *e){
    socket->disconnectFromHost();
}
MainWindow::~MainWindow()
{
    delete ui;
}

