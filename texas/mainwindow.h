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

private:
    Ui::MainWindow *ui;
    QTcpSocket* socket;
    bool tcpisconnect;
    QTextCodec *decoder;
signals:
    void close();
private:
    void initial();
    void write_buffer(QString x);
    void closeEvent(QCloseEvent *e);
    void readAll();
    void tcp_connect();
    void tcp_disconnect();
    void initial_tcp();
    void write_buffer_debug();
};
#endif // MAINWINDOW_H
