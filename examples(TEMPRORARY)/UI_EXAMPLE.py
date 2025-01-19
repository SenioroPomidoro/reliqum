import pygame
import pygame_gui


def exit_action(manager):
    confrimation_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((250, 100), (300, 200)),
        manager=manager,
        window_title="Подтверждение",
        action_long_desc="Вы уверены что хотите выйти из игры?",
        action_short_name="ДА",
        blocking=True  # БЛОКИРУЕТ ЛЮБОЕ НАЖАТИЕ ДО РЕАКЦИИ НА МЕНЮ
    )
    confrimation_dialog.cancel_button.set_text("НЕТ")


def main():
    pygame.init()
    pygame.display.set_caption("Start")
    window_surface = pygame.display.set_mode((800, 600))

    color = "white"

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color("white"))

    manager = pygame_gui.UIManager((800, 600))

    switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (100, 50)),
        text="Switch",
        manager=manager
    )


    red = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 325), (100, 50)),
        text="Red",
        manager=manager
    )

    green = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 375), (100, 50)),
        text="Green",
        manager=manager
    )

    blue = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 425), (100, 50)),
        text="Blue",
        manager=manager
    )

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 525), (100, 50)),
        text="Exit",
        manager=manager
    )

    difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=["Easy", "Medium", "Hard"], starting_option="Easy",
        relative_rect=pygame.Rect((350, 475), (100, 50)),
        manager=manager
    )

    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((325, 50), (150, 50)),
        placeholder_text="ВВЕДИТЕ ИМЯ",
        manager=manager
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_action(manager)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        if color == "black":
                            color = "white"
                        else:
                            color = "black"
                        background.fill((pygame.Color(color)))
                    if event.ui_element == exit_button:
                        exit_action(manager)

                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if event.ui_element == red:
                        background.fill(pygame.Color("Red"))
                    elif event.ui_element == green:
                        background.fill(pygame.Color("Green"))
                    elif event.ui_element == blue:
                        background.fill(pygame.Color("Blue"))
                else:
                    background.fill(pygame.Color(color))

                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    print(event.text)

                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print("Name: ", event.text)

            manager.process_events(event)
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.flip()


if __name__ == "__main__":
    main()
