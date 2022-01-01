import datetime
import logging

import sys

from PySide6.QtCore import QDir, QFile, QObject, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtSql import QSqlDatabase

import sqlDialog

logging.basicConfig(filename='chat.log', level=logging.DEBUG)
logger = logging.getLogger('logger')


def connectToDatabase():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            logger.error("Cannot add database")

    write_dir = QDir("")
    if not write_dir.mkpath("."):
        logger.error("Failed to create writable directory")

    # Ensure that we have a writable location on all devices.
    abs_path = write_dir.absolutePath()
    filename = f"{abs_path}/chat-database.sqlite3"

    # When using the SQLite driver, open() will create the SQLite
    # database if it doesn't exist.
    database.setDatabaseName(filename)
    if not database.open():
        logger.error("Cannot open database")
        QFile.remove(filename)


if __name__ == "__main__":
    app = QGuiApplication()
    connectToDatabase()
    
    engine = QQmlApplicationEngine()
    engine.load(QUrl("chat.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    
    app.exec()
