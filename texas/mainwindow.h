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
    int id;
    //0 待行动
    //1 盖牌
    int all_money;
    int input_money;
    player_information(){}
    player_information(int pos,int _id){position=pos;id=_id;}
};

private:
    Ui::MainWindow *ui;
    QTcpSocket* socket;
    bool tcpisconnect;
    QTextCodec *decoder;
    QMap<QString,int> players;
    QString selfname;


    QMap<QString,player_information> game_player;

signals:
    void close();
private:
    //tcps
    void write_buffer(QString x);
    void closeEvent(QCloseEvent *e);
    void readAll();
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
};
#endif // MAINWINDOW_H
