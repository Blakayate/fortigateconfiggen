import webview

def get_content(window):
    content = window.evaluate_js(
        r"""
        document.querrySelectorAll("input");
        """
    )

    print(content)


window = webview.create_window('Fortigate Config Generator', 'gui/window.html')

webview.start(get_content, window)