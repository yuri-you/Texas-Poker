#include "mainwindow.h"
#include "ui_mainwindow.h"
void MainWindow::Begin_Game(){
    QMessageBox::information(this,"Information!","游戏开始!",QMessageBox::Yes);
    write_buffer("Receive Game Start");
    ui->jiarufangjian->setEnabled(false);
    ui->tuichufangjian->setEnabled(false);
    ui->zhunbei->setEnabled(false);
    ui->quxiaozhunbei->setEnabled(false);
    ui->name->setEnabled(false);
    connect(ui->xiazhu,&QPushButton::clicked,this,&MainWindow::Bet);
    connect(ui->guopai,&QPushButton::clicked,this,&MainWindow::Check);
    connect(ui->qipai,&QPushButton::clicked,this,&MainWindow::Fold);
    connect(ui->all_in,&QPushButton::clicked,this,&MainWindow::All_In);

}
void MainWindow::Iteration_Start(){
    QString youxiweizhi=QString("%1号位").arg(game_player[selfname].position);
    if(game_player[selfname].position==0)youxiweizhi+="(SB)";
    if(game_player[selfname].position==1)youxiweizhi+="(BB)";
    if(game_player[selfname].position==alive_player-1)youxiweizhi+="(庄)";
    ui->youxiweizhi->setText(youxiweizhi);
    ui->dichi->setText(QString("%1").arg(0));
    ui->zuidizhu->setText(QString("%1").arg(0));
    ui->yijingxiazhujine->setText(QString("%1").arg(0));
    ui->xuyaogengzhujine->setText(QString("%1").arg(0));
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
        game_player[datas[1]].all_money=datas[2].toInt();
        if(selfname==datas[1]){
        ui->money->setText(datas[2]);
        }
    }
    else if(datas[0]=="Initial State"){
        game_player.insert(datas[1],player_information(0,datas[2].toInt()));
        alive_player+=1;
        ui->shoujianren->addItem(datas[1]);
    }
    else if(datas[0]=="Initial State Finish"){
        Open_Communication();
    }
    else if(datas[0]=="Information"){
        ui->output->addItem(datas[1]);
    }
    else if(datas[0]=="Initial Position"){
        game_player[datas[1]].position=datas[2].toInt();
    }
    else if(datas[0]=="Initial Position Finish"){
        //开始一轮游戏
        Iteration_Start();
        Show_State();
    }

    else if(datas[0]=="Receive card"){
        display_cards[datas[1].toInt()]->setPixmap(QPixmap(QString("poker//%1.jpg").arg(datas[2])));
    }
    else if(datas[0]=="Activate"){
        Activate(datas[1]);
    }
    else if(datas[0]=="Someone Bet"){
        int money=datas[2].toInt();
        game_player[datas[1]].input_money+=money;
        int dichi=ui->dichi->text().toInt()+money;
        ui->dichi->setText(QString("%1").arg(dichi));
        ui->zuidizhu->setText(QString("%1").arg(game_player[datas[1]].input_money));
        ui->xuyaogengzhujine->setText(QString("%1").arg(game_player[datas[1]].input_money-game_player[selfname].input_money));
        if(datas[1]==selfname){
            int yijingxiazhu=ui->yijingxiazhujine->text().toInt()+money;
            ui->yijingxiazhujine->setText(QString("%1").arg(yijingxiazhu));
        }
        Show_State();
        write_buffer("Accepted");
    }
}
void MainWindow::Activate(QString name){
    game_player[name].state=1;
    if(name==selfname){
        Enable_Bet(true);
    }
    ui->xiazhuwanjia->setText(name);
    QString weizhi=QString("%1号位").arg(game_player[name].position);
    if(game_player[name].position==0)weizhi+="(SB)";
    if(game_player[name].position==1)weizhi+="(BB)";
    if(game_player[name].position==alive_player-1)weizhi+="(庄)";
    ui->xiazhuwanjiaweizhi->setText(weizhi);
    Show_State();
}
void MainWindow::Show_State(){
    ui->player_information->clear();
    for(int i=0;i<game_player.size();++i){
        for(QString name:game_player.keys()){
            if(game_player[name].id==i){
                //昵称
                QString this_name=name;
                if(name==selfname){
                    this_name+="(我)";
                }

                //位置
                QString position=QString("%1号位").arg(game_player[name].position+1);
                switch (game_player[name].position) {
                case 0:position+="(SB)";break;
                case 1:position+="(BB)";break;
                case 2:position+="(枪口)";break;
                }
                if(game_player[name].position==game_player.size()-1){
                    position+="(庄)";
                }

                //行动状态
                QString state;
                switch (game_player[name].state) {
                case 0:state="等待中";break;
                case 1:state="行动中";break;
                case 2:state="已盖牌";break;
                case 3:state="已出局";break;
                }

                //下注金额
                QString bet_money=QString("下注:%1").arg(game_player[name].input_money);
                if(game_player[name].state==3)bet_money="";
                QString output=QString("玩家%1:%2   %3   %6   总金额%5   %4").arg(game_player[name].id+1).arg(this_name).arg(position).arg(bet_money).arg(game_player[name].all_money).arg(state);
                ui->player_information->addItem(output);
            }
        }
    }
}
void MainWindow::Reset_Bet(){
    Disconnect_Bet();
    ui->money_5->setValue(0);
    ui->money_10->setValue(0);
    ui->money_20->setValue(0);
    ui->money_50->setValue(0);
    ui->money_100->setValue(0);
    ui->total_money->setText("0");
    Connect_Bet();
}
void MainWindow::Change_Bet(){
    Disconnect_Bet();
    int m5=ui->money_5->value(),m10=ui->money_10->value(),m20=ui->money_20->value(),m50=ui->money_50->value(),m100=ui->money_100->value();
    int totalmoney=5*m5+10*m10+20*m20+50*m50+100*m100;
    ui->total_money->setText(QString("%1").arg(totalmoney));
    Connect_Bet();
}
void MainWindow::Input_Bet(){
    Disconnect_Bet();
    int total_money=ui->total_money->text().toInt();
    Disconnect_Bet();
    total_money=(total_money/5)*5;
    ui->total_money->setText(QString("%1").arg(total_money));
    ui->money_100->setValue(total_money/100);
    total_money%=100;
    ui->money_50->setValue(total_money/50);
    total_money%=50;
    ui->money_20->setValue(total_money/20);
    total_money%=20;
    ui->money_10->setValue(total_money/10);
    total_money%=10;
    ui->money_5->setValue(total_money/5);
    Connect_Bet();

}
bool MainWindow::Bet_Legal(int a){
    int max_money=ui->money->text().toInt();
    if(a>=max_money){
        Reset_Bet();
        QMessageBox::warning(this,"Warning","金额不足，如果需要请All in!",QMessageBox::Yes);
        return false;
    }
    int min_money=ui->zuidizhu->text().toInt();
    if(min_money>a){
        ui->total_money->setText(ui->zuidizhu->text());
        QMessageBox::warning(this,"Warning",QString("至少下注%1,如果不足请All in!").arg(min_money),QMessageBox::Yes);
        return false;
    }
    return true;
}
void MainWindow::Bet(){
    int total_money=ui->total_money->text().toInt();
    if(Bet_Legal(total_money)){
        QMessageBox::StandardButton signal=QMessageBox::question(this, "确认", QString("将下注%1,确认吗").arg(total_money), QMessageBox::Yes|QMessageBox::No);
        if(signal==QMessageBox::No)return;
        write_buffer(QString("Bet,%1").arg(total_money));
        Enable_Bet(false);
    }
}
void MainWindow::Fold(){
}
void MainWindow::Check(){
}
void MainWindow::All_In(){

}
void MainWindow::Connect_Bet(){
    connect(ui->total_money,&QLineEdit::editingFinished,this,&MainWindow::Input_Bet);
    connect(ui->money_5,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    connect(ui->money_10,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    connect(ui->money_20,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    connect(ui->money_50,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    connect(ui->money_100,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
}
void MainWindow::Disconnect_Bet(){
    disconnect(ui->total_money,&QLineEdit::editingFinished,this,&MainWindow::Input_Bet);
    disconnect(ui->money_5,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    disconnect(ui->money_10,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    disconnect(ui->money_20,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    disconnect(ui->money_50,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
    disconnect(ui->money_100,&QSpinBox::textChanged,this,&MainWindow::Change_Bet);
}
void MainWindow::Enable_Bet(bool signal){
    ui->xiazhu->setEnabled(signal);
    ui->guopai->setEnabled(signal);
    ui->qipai->setEnabled(signal);
    ui->all_in->setEnabled(signal);
}
