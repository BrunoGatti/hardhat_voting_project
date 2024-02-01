import npyscreen

class MyTUI(npyscreen.NPSApp):
    def main(self):
        # Create the form
        form = self.addForm("MAIN", MyForm, name="My TUI")

        # Run the application
        form.edit()

class MyForm(npyscreen.Form):
    def create(self):
        # Add widgets to the form
        self.add(npyscreen.TitleText, name="Enter text:")
        self.button = self.add(npyscreen.ButtonPress, name="Press Me", when_pressed_function=self.button_pressed)

    def button_pressed(self):
        # Function to be executed when the button is pressed
        npyscreen.notify_confirm("Button Pressed!", title="Info")

if __name__ == "__main__":
    app = MyTUI()
    app.run()

