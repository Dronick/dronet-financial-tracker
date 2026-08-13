import json
import os
from datetime import datetime

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.textfield import MDTextField

DATA_FILE = "dronet_data.json"

DEFAULT_DATA = {
    "target_savings": 10000.0,
    "monthly_income": 1200.0,
    "monthly_expenses": 700.0,
    "current_savings": 0.0,
    "history": []
}

KV = '''
MDScreen:
    md_bg_color: 0.08, 0.09, 0.11, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "dronet Financial Tracker"
            font_style: "H5"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint_y: None
            height: "40dp"

        MDCard:
            orientation: "vertical"
            padding: "16dp"
            spacing: "8dp"
            md_bg_color: 0.15, 0.16, 0.20, 1
            radius: [12, 12, 12, 12]
            size_hint_y: None
            height: "180dp"

            MDLabel:
                id: label_target
                text: "Target Goal: $10,000.00"
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1

            MDLabel:
                id: label_balance
                text: "Current Savings: $0.00"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.2, 0.8, 0.4, 1

            MDProgressBar:
                id: progress_bar
                value: 0
                max: 100
                color: 0.2, 0.8, 0.4, 1

            MDLabel:
                id: label_net
                text: "Monthly Net Save: $500.00"
                theme_text_color: "Custom"
                text_color: 0.7, 0.7, 0.7, 1

            MDLabel:
                id: label_time
                text: "Estimated Time: Calculating..."
                theme_text_color: "Custom"
                text_color: 0.7, 0.7, 0.7, 1

        MDBoxLayout:
            orientation: 'horizontal'
            spacing: "10dp"
            size_hint_y: None
            height: "60dp"

            MDTextField:
                id: input_amount
                hint_text: "Enter Deposit Amount"
                mode: "rectangle"
                input_filter: "float"
                line_color_focus: 0.2, 0.8, 0.4, 1
                text_color_focus: 1, 1, 1, 1

            MDRaisedButton:
                text: "Deposit"
                md_bg_color: 0.2, 0.8, 0.4, 1
                pos_hint: {"center_y": 0.5}
                on_release: app.make_deposit()

        MDRaisedButton:
            text: "View Transaction History"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.5, 0.8, 1
            on_release: app.show_history_dialog()

        Widget:
'''


class DronetApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.data = self.load_data()
        return Builder.load_string(KV)

    def on_start(self):
        self.refresh_ui()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.save_data(DEFAULT_DATA)
            return dict(DEFAULT_DATA)
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def refresh_ui(self):
        target = self.data["target_savings"]
        current = self.data["current_savings"]
        income = self.data["monthly_income"]
        expenses = self.data["monthly_expenses"]
        net_monthly = income - expenses
        remaining = max(0.0, target - current)

        percent = (current / target) * 100 if target > 0 else 0

        self.root.ids.label_target.text = f"Target Goal: ${target:,.2f}"
        self.root.ids.label_balance.text = f"Current Savings: ${current:,.2f}"
        self.root.ids.label_net.text = (
            f"Monthly Net Save: ${net_monthly:,.2f} "
            f"(Income: ${income:,.2f} | Exp: ${expenses:,.2f})"
        )
        self.root.ids.progress_bar.value = min(100, percent)

        if remaining <= 0:
            self.root.ids.label_time.text = "Goal Reached! \U0001F389"
        elif net_monthly <= 0:
            self.root.ids.label_time.text = (
                "Estimated Time: Not saving enough to reach goal"
            )
        else:
            months_left = remaining / net_monthly
            self.root.ids.label_time.text = (
                f"Estimated Time: {months_left:.1f} months remaining"
            )

    def make_deposit(self):
        val = self.root.ids.input_amount.text
        if not val:
            return
        try:
            amount = float(val)
        except ValueError:
            return

        if amount > 0:
            self.data["current_savings"] += amount
            entry = {
                "type": "deposit",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.data["history"].append(entry)
            self.save_data(self.data)
            self.refresh_ui()
            self.root.ids.input_amount.text = ""

    def show_history_dialog(self):
        if not self.data["history"]:
            history_text = "No transactions recorded yet."
        else:
            lines = []
            for item in reversed(self.data["history"]):
                lines.append(
                    f"[{item['date']}] {item['type'].upper()}: "
                    f"+${item['amount']:.2f}"
                )
            history_text = "\n".join(lines)

        self.dialog = MDDialog(
            title="Transaction History",
            text=history_text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=(0.2, 0.8, 0.4, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()


if __name__ == "__main__":
    DronetApp().run()
