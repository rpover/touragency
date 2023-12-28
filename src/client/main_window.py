from PySide6 import QtWidgets, QtCore, QtGui
from src.client.login_form import LoginWindow
from src.client.register_form import RegisterWindow
from src.client.tools import get_pixmap_path
from src.client.api.session import Session
from src.client.tour_edit_form import TourEdit
from src.client.tour_cteate_form import TourCreate
import src.client.api.resolvers
from src.server.database.models import User, Ticket
import threading
import datetime

session: Session = Session()
main_win = None


def include_widgets_by_pl(element: dict[str, QtWidgets.QWidget]):
    global session

    for key, item in element.items():
        if not issubclass(type(item), QtWidgets.QWidget):
            continue

        if item.property('power_level') is not None:
            item.show() if session.user.power_level >= item.property('power_level') else item.hide()

        include_widgets_by_pl(item.__dict__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        try:
            if 'error' in self.__connect_check():
                print('Server not available')
                exit()
        except TypeError:
            pass

        self.__initUi()
        self.__setupUi()
        self.show()

    @src.client.api.resolvers.server_available
    def __connect_check(self) -> None:
        return None

    def __initUi(self) -> None:
        self.central_widget = QtWidgets.QWidget()
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.page_list = PageListMenu()
        self.widget_container = QtWidgets.QWidget()
        self.widget_container_layout = QtWidgets.QVBoxLayout()
        self.tour_list = TourList()
        self.ticket_list = TicketList()
        self.country_list = CountryList()
        self.authorization_menu = AuthorizationMenu()
        self.user_profile = UserProfile()

    def __setupUi(self) -> None:
        self.resize(930, 615)
        self.setWindowTitle('Tour agency Client')
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_h_layout)
        self.widget_container.setLayout(self.widget_container_layout)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_h_layout.addWidget(self.page_list)
        self.main_h_layout.addWidget(self.widget_container)
        self.main_h_layout.addWidget(self.authorization_menu)
        self.main_h_layout.addWidget(self.user_profile)

        self.widget_container_layout.addWidget(self.tour_list)
        self.widget_container_layout.addWidget(self.ticket_list)
        self.widget_container_layout.addWidget(self.country_list)

        self.page_list.tour_item.bind_widget(self.tour_list)
        self.page_list.ticket_item.bind_widget(self.ticket_list)
        self.page_list.country_item.bind_widget(self.country_list)

        include_widgets_by_pl(self.__dict__)
        global main_win
        main_win = self
        self.user_profile.hide()

        self.page_list.tour_item.switch_page()

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        messagebox = QtWidgets.QMessageBox(self if not parent else parent)
        messagebox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        messagebox.setWindowTitle("Error" if error else "Information")
        messagebox.setText(text)
        messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical if error else QtWidgets.QMessageBox.Icon.Information)
        messagebox.show()

    def set_session(self, new_session: Session):
        global session
        session = new_session
        self.authorization()

    def authorization(self):
        self.authorization_menu.hide()
        self.user_profile.show()
        self.user_profile.fill_line_edits()
        self.ticket_list.update_tickets()
        self.country_list.update_countries()

        include_widgets_by_pl(self.__dict__)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.tour_list.stop_flag = True
        self.ticket_list.stop_flag = True
        self.country_list.stop_flag = True
        exit()


class PageListMenu(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tour_item = MenuItem()
        self.ticket_item = MenuItem()
        self.country_item = MenuItem()

    def __setupUi(self) -> None:
        self.setMaximumWidth(150)
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_v_layout.setContentsMargins(5, 5, 5, 5)
        self.opened_widget = self.tour_item

        self.tour_item.setup('tour.png', 'Tours')
        self.ticket_item.setup('ticket.png', 'Tickets')
        self.country_item.setup('country.png', 'Countries')

        self.main_v_layout.addWidget(self.tour_item)
        self.main_v_layout.addWidget(self.ticket_item)
        self.main_v_layout.addWidget(self.country_item)

        self.tour_item.setProperty('power_level', 0)
        self.ticket_item.setProperty('power_level', 1)
        self.country_item.setProperty('power_level', 3)


class MenuItem(QtWidgets.QFrame):
    connection_def = None
    widget: QtWidgets.QWidget = None

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.container_widget = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QHBoxLayout()
        self.icon = QtWidgets.QLabel()
        self.title = QtWidgets.QLabel()

    def __setupUi(self) -> None:
        self.setLayout(self.main_h_layout)
        self.main_h_layout.addWidget(self.container_widget)
        self.container_widget.setLayout(self.container_layout)
        self.main_h_layout.setContentsMargins(5, 5, 5, 5)
        self.container_layout.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        self.title.setStyleSheet('color: black')

        self.container_layout.addWidget(self.icon)
        self.container_layout.addWidget(self.title)
        self.icon.setFixedSize(32, 32)

    def setup(self, icon_name: str, title: str):
        self.set_icon(icon_name)
        self.set_title(title)

    def set_icon(self, icon_name: str) -> None:
        self.icon.setPixmap(QtGui.QPixmap(get_pixmap_path(icon_name)))

    def set_title(self, title: str) -> None:
        self.title.setText(title)

    def bind_widget(self, widget: QtWidgets.QWidget):
        self.widget = widget

    def on_mouse_enter(self):
        self.setStyleSheet('QFrame{background-color: darkgray; border-radius: 15px}')
        self.title.setStyleSheet('color: white')

    def on_mouse_leave(self):
        self.setStyleSheet('QFrame{background-color: none; border-radius: 15px}')
        self.title.setStyleSheet('color: black')

    def on_mouse_clicked(self):
        self.switch_page()
        if self.connection_def:
            self.connection_def()

    def connect_function(self, foo):
        self.connection_def = foo

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        self.on_mouse_enter()

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.on_mouse_leave()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.on_mouse_clicked()

    def switch_page(self):
        for item in self.parent().__dict__:
            page: MenuItem = self.parent().__dict__[item]

            if type(page) == MenuItem:
                page.widget.show() if page == self else page.widget.hide()


class TourList(QtWidgets.QWidget):
    add_tour_signal = QtCore.Signal(str, str, str, str)
    stop_flag: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tool_h_layout = QtWidgets.QHBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.create_tour_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_h_layout.setContentsMargins(0, 10, 0, 0)
        self.tool_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.main_v_layout.addLayout(self.tool_h_layout)
        self.tool_h_layout.addWidget(self.create_tour_button)
        self.main_v_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.create_tour_button.setIcon(QtGui.QPixmap(get_pixmap_path('add.png')))
        self.create_tour_button.setFixedSize(24, 24)
        self.create_tour_button.setProperty('power_level', 2)

        self.create_tour_button.clicked.connect(self.create_tour)
        self.add_tour_signal.connect(self.add_tour_slot)

        self.update_tours()

    def create_tour(self) -> None:
        TourCreate(self)

    def update_tours(self):
        self.clear_tours()
        threading.Thread(target=self.load_tours).start()

    def load_tours(self) -> None:
        for tour in src.client.api.resolvers.get_all_tours():
            if self.stop_flag:
                exit()

            country = src.client.api.resolvers.get_country_by_id(int(tour['country_id']))['name']

            if not country:
                continue

            self.add_tour_signal.emit(
                str(tour['id']),
                country,
                str(tour['hours']),
                str(tour['price']))

    def add_tour(self, tour_id: str, country: str, hours: str, price: str) -> None:
        new_tour = TourItem()
        new_tour.set_tour_info(tour_id, country, hours, price)

        self.scroll_widget.__dict__.update({tour_id: new_tour})
        self.scroll_layout.addWidget(new_tour)

    def clear_tours(self):
        for tour in dict(self.scroll_widget.__dict__):
            if type(self.scroll_widget.__dict__[tour]) == TourItem:
                self.scroll_widget.__dict__[tour].close()
                self.scroll_widget.__dict__.pop(tour)

    @QtCore.Slot(str, str, str, str)
    def add_tour_slot(self, tour_id: str, country: str, hours: str, price: str) -> None:
        self.add_tour(tour_id, country, hours, price)
        include_widgets_by_pl(self.__dict__)


class TourItem(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.country = QtWidgets.QLabel()
        self.hours = QtWidgets.QLabel()
        self.price = QtWidgets.QLabel()
        self.buy_button = QtWidgets.QPushButton()
        self.edit_button = QtWidgets.QPushButton()
        self.delete_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.main_h_layout.addWidget(self.country)
        self.main_h_layout.addWidget(self.hours)
        self.main_h_layout.addWidget(self.price)
        self.main_h_layout.addWidget(self.buy_button)
        self.main_h_layout.addWidget(self.edit_button)
        self.main_h_layout.addWidget(self.delete_button)

        self.buy_button.setText('Buy')
        self.edit_button.setIcon(QtGui.QPixmap(get_pixmap_path('edit.png')))
        self.delete_button.setIcon(QtGui.QPixmap(get_pixmap_path('delete.png')))
        self.edit_button.setProperty('power_level', 2)
        self.delete_button.setProperty('power_level', 2)
        self.buy_button.setProperty('power_level', 1)

        self.country.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)
        self.price.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)
        self.hours.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)

        self.buy_button.setFixedWidth(40)
        self.edit_button.setFixedSize(24, 24)
        self.delete_button.setFixedSize(24, 24)

    def set_tour_info(self, tour_id: int, country: str, hours: str, price: str) -> None:
        self.country.setText(country)
        self.hours.setText(hours)
        self.price.setText(price)
        self.buy_button.clicked.connect(lambda: self.buy_ticket(tour_id))
        self.edit_button.clicked.connect(lambda: self.edit_tour(tour_id))
        self.delete_button.clicked.connect(lambda: self.delete_tour(tour_id))

    def buy_ticket(self, tour_id: int) -> None:
        global main_win

        main_win.page_list.ticket_item.widget.new_ticket(tour_id)

    def edit_tour(self, tour_id: int) -> None:
        global main_win

        TourEdit(self, tour_id)

    def delete_tour(self, tour_id: int) -> None:
        src.client.api.resolvers.delete_tour(tour_id)
        self.tour_updated()

    def tour_updated(self):
        global main_win

        main_win.tour_list.update_tours()
        main_win.ticket_list.update_tickets()


class TicketList(QtWidgets.QWidget):
    stop_flag: bool = False
    add_ticket_signal: QtCore.Signal = QtCore.Signal(int, str, datetime.datetime, datetime.datetime)

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.tool_h_layout = QtWidgets.QHBoxLayout()
        self.user_search_line_edit = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_h_layout.setContentsMargins(10, 10, 10, 0)
        self.main_v_layout.addLayout(self.tool_h_layout)
        self.tool_h_layout.addWidget(self.user_search_line_edit)
        self.tool_h_layout.addWidget(self.search_button)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.main_v_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.search_button.setMaximumSize(24, 24)
        self.search_button.setIcon(QtGui.QPixmap(get_pixmap_path('search.png')))

        self.search_button.clicked.connect(self.on_find_button_click)
        self.add_ticket_signal.connect(self.add_ticket)

        self.user_search_line_edit.setProperty('power_level', 3)
        self.search_button.setProperty('power_level', 3)

    def new_ticket(self, tour_id: int):
        global session

        tour_info = src.client.api.resolvers.get_tour_by_id(tour_id)
        date_start = datetime.datetime.now()
        date_end = date_start + datetime.timedelta(hours=int(tour_info['hours']))

        new_ticket = Ticket(
            tour_id=tour_id,
            date_start=str(date_start),
            date_end=str(date_end),
            user_id=session.user.id
        )

        src.client.api.resolvers.new_ticket(new_ticket)

        self.update_tickets()

    def on_find_button_click(self):
        global main_win, session

        if not self.user_search_line_edit.text().isdigit():
            return main_win.show_error(
                text='Search field must contains id',
                error=True,
                parent=self
            )

        self.update_tickets(int(self.user_search_line_edit.text()))

    def update_tickets(self, replaced_id: int = 0) -> None:
        self.clear_tickets()
        threading.Thread(target=self.load_tickets, args=(replaced_id, )).start()

    def load_tickets(self, replaced_id: int = 0) -> None:
        global session

        for ticket in src.client.api.resolvers.get_all_tickets():
            if self.stop_flag:
                exit()

            if replaced_id == 0:
                if ticket['user_id'] != session.user.id:
                    continue
            else:
                if ticket['user_id'] != replaced_id:
                    continue

            country = src.client.api.resolvers.get_tour_by_id(ticket['tour_id'])

            if not country:
                continue

            country = src.client.api.resolvers.get_country_by_id(int(country['country_id']))['name']

            self.add_ticket_signal.emit(
                ticket['id'],
                country,
                ticket['date_start'],
                ticket['date_end']
            )

    def add_ticket(self, ticket_id, country, date_start, date_end) -> None:
        new_ticket = TicketItem()

        self.scroll_widget.__dict__.update({ticket_id: new_ticket})
        new_ticket.set_ticket_info(ticket_id, country, date_start, date_end)
        self.scroll_layout.addWidget(new_ticket)

        include_widgets_by_pl(self.__dict__)

    def clear_tickets(self) -> None:
        for ticket in dict(self.scroll_widget.__dict__):
            if type(self.scroll_widget.__dict__[ticket]) == TicketItem:
                self.scroll_widget.__dict__[ticket].close()
                self.scroll_widget.__dict__.pop(ticket)

    @QtCore.Slot(int, str, datetime.datetime, datetime.datetime)
    def add_ticket_slot(self, ticket_id: int, country: str, date_start: datetime.datetime, date_end: datetime.datetime):
        self.add_ticket(ticket_id, country, date_start, date_end)
        include_widgets_by_pl(self.__dict__)

    def delete_ticket(self, ticket_id: int) -> None:
        src.client.api.resolvers.delete_ticket(ticket_id)


class TicketItem(QtWidgets.QWidget):
    now_edit: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.country = QtWidgets.QLabel()
        self.country_combo_box = QtWidgets.QComboBox()
        self.date_start = QtWidgets.QLabel()
        self.date_end = QtWidgets.QLabel()
        self.edit_button = QtWidgets.QPushButton()
        self.delete_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.main_h_layout.addWidget(self.country)
        self.main_h_layout.addWidget(self.country_combo_box)
        self.main_h_layout.addWidget(self.date_start)
        self.main_h_layout.addWidget(self.date_end)
        self.main_h_layout.addWidget(self.edit_button)
        self.main_h_layout.addWidget(self.delete_button)

        self.edit_button.setIcon(QtGui.QPixmap(get_pixmap_path('edit.png')))
        self.delete_button.setIcon(QtGui.QPixmap(get_pixmap_path('delete.png')))
        self.edit_button.setFixedSize(24, 24)
        self.delete_button.setFixedSize(24, 24)

        self.edit_button.setProperty('power_level', 3)

        self.country.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_start.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_end.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.country_combo_box.hide()

    def set_ticket_info(self, ticket_id: int, country: str, date_start, date_end) -> None:
        date_start = date_start[:10].replace('-', '.')
        date_end = date_end[:10].replace('-', '.')

        self.country.setText(country)
        self.date_start.setText(date_start)
        self.date_end.setText(date_end)

        self.edit_button.clicked.connect(lambda: self.edit(ticket_id))
        self.delete_button.clicked.connect(lambda: self.delete(ticket_id))

    def edit(self, ticked_id):
        global session

        self.now_edit = not self.now_edit

        if self.now_edit:
            for tour in src.client.api.resolvers.get_all_tours():
                country = src.client.api.resolvers.get_country_by_id(tour['country_id'])
                country = f'{country["id"]} : {country["name"]}'
                self.country_combo_box.insertItem(self.country_combo_box.count(), country)

        else:
            ticket = Ticket(
                id=ticked_id,
                tour_id=int(self.country_combo_box.currentText().replace(' ', '').split(':')[0]),
                user_id=int(src.client.api.resolvers.get_ticket_by_id(ticked_id)['user_id']),
                date_start=self.date_start.text(),
                date_end=self.date_end.text()
            )

            src.client.api.resolvers.update_ticket(ticket)

            answer = src.client.api.resolvers.get_ticket_by_id(ticked_id)

            self.country.setText(self.country_combo_box.currentText().replace(' ', '').split(':')[1])

            date_start = answer['date_start'][:10].replace('-', '.')
            date_end = answer['date_end'][:10].replace('-', '.')

            self.date_start.setText(date_start)
            self.date_end.setText(date_end)

            self.country_combo_box.clear()

        self.country.setHidden(self.now_edit)
        self.country_combo_box.setHidden(not self.now_edit)

    def delete(self, ticket_id: int) -> None:
        src.client.api.resolvers.delete_ticket(ticket_id)
        self.parent().__dict__[ticket_id].close()
        self.parent().__dict__.pop(ticket_id)


class CountryList(QtWidgets.QWidget):
    stop_flag: bool = False
    add_country_signal: QtCore.Signal = QtCore.Signal(int, str)

    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.main_v_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

        self.add_country_signal.connect(self.add_country_slot)

    @QtCore.Slot(int, str)
    def add_country_slot(self, country_id: int, name: str):
        self.add_country(country_id, name)
        include_widgets_by_pl(self.__dict__)

    def add_country(self, country_id: int, name: str):
        new_country = CountryItem()
        new_country.set_country_info(country_id, name)

        self.scroll_widget.__dict__.update({country_id: new_country})
        self.scroll_layout.addWidget(new_country)

    def update_countries(self) -> None:
        threading.Thread(target=self.load_countries).start()

    def load_countries(self) -> None:
        global session

        self.clear_countries()

        for country in src.client.api.resolvers.get_all_countries():
            if self.stop_flag:
                exit()

            self.add_country_signal.emit(
                int(country['id']),
                country['name']
            )

    def clear_countries(self) -> None:
        for country in dict(self.scroll_widget.__dict__):
            if type(self.scroll_widget.__dict__[country]) == CountryItem:
                self.scroll_widget.__dict__[country].close()
                self.scroll_widget.__dict__.pop(country)


class CountryItem(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.id = QtWidgets.QLabel()
        self.name = QtWidgets.QLabel()
        self.edit_button = QtWidgets.QPushButton()
        self.delete_button = QtWidgets.QToolButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.main_h_layout.addWidget(self.id)
        self.main_h_layout.addWidget(self.name)
        self.main_h_layout.addWidget(self.edit_button)
        self.main_h_layout.addWidget(self.delete_button)

        self.edit_button.setIcon(QtGui.QPixmap(get_pixmap_path('edit.png')))
        self.edit_button.setFixedSize(24, 24)
        self.delete_button.setIcon(QtGui.QPixmap(get_pixmap_path('delete.png')))
        self.delete_button.setFixedSize(24, 24)

        self.id.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def set_country_info(self, country_id: int, name: str) -> None:
        self.id.setText(str(country_id))
        self.name.setText(name)

        self.edit_button.clicked.connect(lambda: self.edit_country(country_id))
        self.delete_button.clicked.connect(lambda: self.delete_country(country_id))

    def edit_country(self, country_id: int) -> None:
        pass

    def delete_country(self, country_id: int) -> None:
        pass


class AuthorizationMenu(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.login_button = QtWidgets.QPushButton()
        self.register_button = QtWidgets.QPushButton()

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.setMaximumWidth(120)

        self.main_v_layout.addWidget(self.login_button)
        self.main_v_layout.addWidget(self.register_button)

        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.login_button.setText('Login')
        self.register_button.setText('Register')

        self.login_button.clicked.connect(self.on_login_click)
        self.register_button.clicked.connect(self.on_register_click)

    def on_login_click(self) -> None:
        self.open_login_dialog()

    def on_register_click(self) -> None:
        self.open_register_dialog()

    def open_login_dialog(self):
        LoginWindow(self.parent().parent())  # Надеюсь увидеть этот комментарий и всё-таки отрефакторить код

    def open_register_dialog(self):
        RegisterWindow(self)

    def show_message(self, text: str, error: bool = False, parent=None) -> None:
        self.parent().parent().show_message(
            text=text,
            error=error,
            parent=parent
        )


class UserProfile(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__initUi()
        self.__setupUi()

    def __initUi(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()

        self.name_layout = QtWidgets.QHBoxLayout()
        self.surname_layout = QtWidgets.QHBoxLayout()
        self.phone_layout = QtWidgets.QHBoxLayout()
        self.password_layout = QtWidgets.QHBoxLayout()
        self.confirm_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.name_label = QtWidgets.QLabel()
        self.surname_label = QtWidgets.QLabel()
        self.phone_label = QtWidgets.QLabel()
        self.password_label = QtWidgets.QLabel()
        self.confirm_password_label = QtWidgets.QLabel()
        self.power_level_label = QtWidgets.QLabel()
        self.user_id_label = QtWidgets.QLabel()

        self.name_line_edit = QtWidgets.QLineEdit()
        self.surname_line_edit = QtWidgets.QLineEdit()
        self.phone_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit = QtWidgets.QLineEdit()
        self.confirm_password_line_edit = QtWidgets.QLineEdit()

        self.edit_button = QtWidgets.QPushButton()
        self.allow_button = QtWidgets.QPushButton()

        self.spacer = QtWidgets.QSpacerItem(0, 10)

    def __setupUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.setMaximumWidth(250)
        self.main_v_layout.addLayout(self.name_layout)
        self.main_v_layout.addLayout(self.surname_layout)
        self.main_v_layout.addLayout(self.phone_layout)
        self.main_v_layout.addSpacerItem(self.spacer)
        self.main_v_layout.addLayout(self.password_layout)
        self.main_v_layout.addLayout(self.confirm_layout)
        self.main_v_layout.addWidget(self.power_level_label)
        self.main_v_layout.addWidget(self.user_id_label)
        self.main_v_layout.addSpacerItem(self.spacer)
        self.main_v_layout.addLayout(self.button_layout)

        self.name_layout.addWidget(self.name_label)
        self.surname_layout.addWidget(self.surname_label)
        self.phone_layout.addWidget(self.phone_label)
        self.password_layout.addWidget(self.password_label)
        self.confirm_layout.addWidget(self.confirm_password_label)

        self.name_layout.addWidget(self.name_line_edit)
        self.surname_layout.addWidget(self.surname_line_edit)
        self.phone_layout.addWidget(self.phone_line_edit)
        self.password_layout.addWidget(self.password_line_edit)
        self.confirm_layout.addWidget(self.confirm_password_line_edit)

        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.allow_button)

        self.edit_button.setText('Edit')
        self.allow_button.setText('Allow')

        self.name_label.setText('Name:')
        self.surname_label.setText('Surname:')
        self.phone_label.setText('Phone:')
        self.password_label.setText('Password:')
        self.confirm_password_label.setText('Confirm:')
        self.power_level_label.setText('Power level: 0')
        self.user_id_label.setText('ID: 0')

        self.name_line_edit.setFixedWidth(150)
        self.surname_line_edit.setFixedWidth(150)
        self.phone_line_edit.setFixedWidth(150)
        self.password_line_edit.setFixedWidth(150)
        self.confirm_password_line_edit.setFixedWidth(150)

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.set_line_edit_enable(False)

        self.allow_button.setEnabled(False)

        self.edit_button.clicked.connect(self.on_edit_click)
        self.allow_button.clicked.connect(self.on_allow_click)

    def set_line_edit_enable(self, enabled: bool) -> None:
        self.name_line_edit.setEnabled(enabled)
        self.surname_line_edit.setEnabled(enabled)
        self.phone_line_edit.setEnabled(enabled)
        self.password_line_edit.setEnabled(enabled)
        self.confirm_password_line_edit.setEnabled(enabled)

    def fill_line_edits(self) -> None:
        global session

        self.name_line_edit.setText(session.user.name)
        self.surname_line_edit.setText(session.user.surname)
        self.phone_line_edit.setText(session.user.phone)
        self.password_line_edit.setText(session.user.password)
        self.power_level_label.setText(f'Power level: {str(session.user.power_level)}')
        self.user_id_label.setText(f'ID: {str(session.user.id)}')

    def on_edit_click(self) -> None:
        self.edit_button.setEnabled(False)
        self.allow_button.setEnabled(True)

        self.set_line_edit_enable(True)

    def validate_password(self) -> bool:
        global session
        return self.confirm_password_line_edit.text() == self.password_line_edit.text()

    def on_allow_click(self) -> None:
        global session

        if not self.validate_password():
            return self.parent().parent().show_message(
                text='Incorrect confirm password',
                error=True,
                parent=self
            )

        user = User(
            id=session.user.id,
            name=self.name_line_edit.text(),
            surname=self.surname_line_edit.text(),
            phone=self.phone_line_edit.text(),
            password=self.password_line_edit.text(),
            power_level=session.user.power_level
        )

        session.update(user)

        if session.error:
            return self.parent().parent().show_message(
                text=session.error,
                error=True,
                parent=self
            )

        self.set_line_edit_enable(False)
        self.allow_button.setEnabled(False)
        self.edit_button.setEnabled(True)
