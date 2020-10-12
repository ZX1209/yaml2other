import PySimpleGUIQt as sg
from class_yaml2dot import tran_yaml_str2dot_str
from yaml2mermaid import tran_yaml_str2mermaid_str

import logging as log

log.basicConfig(level=log.DEBUG)
log.debug("this is a demo massage")

sg.theme("DarkAmber")  # Add a touch of color
# All the stuff inside your window.
layout = [
    [
        sg.Multiline(
            key="in_yaml",
            size=(400, 300),
            enable_events=True,
            auto_size_text=True,
            default_text="input yaml here",
            # do_not_clear=False,
        ),
        sg.Column(
            [
                [sg.Button("tranDot")],
                [sg.Button("tranMermaid")],
                [sg.Button("tran bottom here")],
            ]
        ),
        sg.MultilineOutput(
            size=(400, 300),
            key="out_dot",
            auto_size_text=True,
            default_text="output will be here",
            font=[sg.DEFAULT_FONT[0], 14],
        ),
    ],
]

# Create the Window
window = sg.Window(
    "yaml2other gui",
    layout,
    font=[sg.DEFAULT_FONT[0], 14],
)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    tran_str = ""
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    elif event == "tranDot":
        tran_str = tran_yaml_str2dot_str(values["in_yaml"])
    elif event == "tranMermaid":
        tran_str = tran_yaml_str2mermaid_str(values["in_yaml"])

    window["out_dot"].update(tran_str)

    log.debug((event, values))


window.close()
