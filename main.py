from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior




class Menu(ButtonBehavior, BoxLayout):
    def btn_clc(self):
        PongApp().stop()
        #PongApp().run()

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):

    ball = ObjectProperty(None)
    menu = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        if self.player1.score >= 10:
            Clock.unschedule(self.update)

            self.win_label = Label(size_hint=(None, None),
                              text = 'Winner is Player1!',
                              markup=True, font_size=70, color=[1,0,0,1])
            self.win_label.center = self.center

            self.win_label.bind()
            self.win_label.texture_update()
            self.add_widget(self.win_label)

        if self.player2.score >= 10:
            Clock.unschedule(self.update)

            self.win_label = Label(size_hint=(None, None),
                              text = 'Winner is Player2!',
                              markup=True, font_size=70, color=[1,0,0,1])
            self.win_label.center = self.center

            self.win_label.bind()
            self.win_label.texture_update()
            self.add_widget(self.win_label)


    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        self.game = PongGame()
        self.game.serve_ball()
        self.event = Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        return self.game

    def on_pause(self):
        self.event.cancel()


    def on_resume(self):
        self.event = Clock.schedule_interval(self.game.update, 1.0 / 60.0)


if __name__ == '__main__':
    PongApp().run()
