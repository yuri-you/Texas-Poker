#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include<QTextCodec>
#include<QMessageBox>
//#include<QTcp
#include<QTcpSocket>
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
struct player_information{
    int position;
    int state;
    /*
     0 待行动
     1 行动中
     2 盖牌
     3 出局
    */
    int id;
    int all_money;
    int input_money=0;
    player_information(){}
    player_information(int pos,int _id){position=pos;id=_id;state=0;}
};

private:
    Ui::MainWindow *ui;
    QTcpSocket* socket;
    bool tcpisconnect;
    QTextCodec *decoder;
    QMap<QString,int> players;
    QString selfname;
    QVector<QLabel*> display_cards;
    int alive_player=0;
    QMap<QString,player_information> game_player;


signals:
    void close();
private:
    //connect link
    void Connect_Bet();
    void Disconnect_Bet();

    //tcps
    void write_buffer(QString x);
    void closeEvent(QCloseEvent *e);
    void read();
    void readAll(QString data);
    void tcp_connect();
    void tcp_disconnect();
    void initial_tcp();
    void write_buffer_debug();
    void modify_user();
    void ready();
    void cancel_ready();
    void change_name();
    void change_host();

    //layouts
    void initial();
    void initial_cards();
    void initial_lineedit();

    //game
    void Receive_Game_Instruction(QStringList x);
    void Show_State();
    void Begin_Game();
    void Open_Communication();
    void Send_Message();
    void Clear_Message();
    void Activate(QString name);
    void Bet();
    void Fold();
    void All_In();
    void Check();
    void Iteration_Start();
    void Change_Bet();
    void Input_Bet();
    void Reset_Bet();
    bool Bet_Legal(int a);
    void Enable_Bet(bool signal);
    void Reset_Card();
    void Reset_Information();
};
#endif // MAINWINDOW_H
