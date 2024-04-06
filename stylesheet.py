stylesheet = """
    /* the Dark Theme */
    QWidget {
        background-color: #333333;
        color: #e0e0e0; /* Lighter text for better readability */
    }

    /* QPushButton */
    QPushButton {
        border: 2px solid #556677;
        border-radius: 6px;
        color: #ffffff;
        padding: 5px 10px;
        font-size: 16px;
        background-color: #556677;
    }
    QPushButton:pressed {
        background-color: #445566;
    }
    QPushButton:hover {
        border: 2px solid #778899;
        background-color: #667788;
    }

    /* QToolButton */
    QToolButton {
        border: 2px solid #8f8f91;
        border-radius: 6px;
        background-color: #556677;
        color: #ffffff;
        padding: 2px;
    }
    QToolButton:pressed {
        background-color: #445566;
    }
    QToolButton:hover {
        border: 2px solid #1c1c1c;
    }

    /* QSpinBox */
    QSpinBox {
        width: 80px; 
        height: 30px; 
        font-size: 20px;
    }

"""
