#include "mainwindow.h"
#include "ui_mainwindow.h"
void MainWindow::Begin_Game(){
    QMessageBox::information(this,"Information!","游戏开始!",QMessageBox::Yes);
    write_buffer("Receive Game Start");
    ui->jiarufangjian->setEnabled(false);
    ui->tuichufangjia->setEnabled(false);
    ui->zhunbei->setEnabled(false);
    ui->quxiaozhunbei->setEnabled(false);
    ui->name->setEnabled(false);
}
void MainWindow::Clear_Message(){
    ui->output->clear();
}
void MainWindow::Open_Communication(){
    ui->shoujianren->addItem("全体成员");
    ui->fasongneirong->setEnabled(true);
    ui->fasongxiaoxi->setEnabled(true);
    ui->shoujianren->setEnabled(true);
    ui->qingkongxiaoxi->setEnabled(true);
    connect(ui->fasongxiaoxi,&QPushButton::clicked,this,&MainWindow::Send_Message);
    connect(ui->qingkongxiaoxi,&QPushButton::clicked,this,&MainWindow::Clear_Message);
}
void MainWindow::Send_Message(){
    QString text=ui->fasongneirong->text();
    qDebug()<<"发送内容:"<<text;
    if(text.isEmpty()){
        QMessageBox::warning(this,"Warning!","输入内容为空!",QMessageBox::Yes);
        return;
    }
    if(ui->shoujianren->currentText()=="全体成员"){
        for(QString shoujianren:game_player.keys()){
            if(shoujianren!=selfname){
                write_buffer(QString("Information,%1,%3:%2").arg(shoujianren).arg(text).arg(shoujianren));
                ui->output->addItem(QString("<全体消息>%1(我):%2").arg(selfname).arg(text));
            }
        }
    }
    else{
        write_buffer(QString("Information,%1,%3:%2").arg(ui->shoujianren->currentText()).arg(text).arg(selfname));
        ui->output->addItem(QString("%1(我):%2").arg(selfname).arg(text));
    }
    ui->fasongneirong->clear();
}
void MainWindow::Receive_Game_Instruction(QStringList datas){
    if(datas[0]=="Begin Game"){
        Begin_Game();
    }
    else if(datas[0]=="Change Money"){
        ui->money->setText(datas[1]);
    }
    else if(datas[0]=="Initial State"){
        game_player.insert(datas[1],player_information(datas[3].toInt(),datas[2].toInt()));
        ui->shoujianren->addItem(datas[1]);
//        write_buffer("Accepted");
    }
    else if(datas[0]=="Initial State Finish"){
        Show_State();
        Open_Communication();
//        write_buffer("Accepted");
    }
    else if(datas[0]=="Information"){
//        ui->output->clear();
//        QListWidgetItem t(datas[1],)
        ui->output->addItem(datas[1]);
    }
}
void MainWindow::Show_State(){
    int length=16;
    ui->player_information->clear();
    for(int i=0;i<game_player.size();++i){
        for(QString name:game_player.keys()){
            if(game_player[name].id==i){
                QString this_name=name;
                if(name==selfname){
                    this_name+="(我)";
                }
                QString t(length-selfname.size(),' ');
                this_name+=t;
                QString position=QString("%1号位").arg(game_player[name].position+1);
                switch (game_player[name].position) {
                case 0:position+="(SB)";break;
                case 1:position+="(BB)";break;
                case 2:position+="(枪口)";break;
                }
                if(game_player[name].position==game_player.size()-1){
                    position+="(庄)";
                }
                QString output=QString("玩家%1:%2 %3").arg(game_player[name].id+1).arg(this_name).arg(position);
                ui->player_information->addItem(output);
            }
        }
    }
}
