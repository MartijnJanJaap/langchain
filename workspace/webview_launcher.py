# filename: webview_launcher.py

import webview
import stock_tracker
import config  # Ensure config is imported

class Api:
    def runStockTracker(self):
        stock_tracker.main()

if __name__ == '__main__':
    # Make sure that config.output_html_path is defined. If not, use a direct file path where the HTML is saved.
    window = webview.create_window('CSV Report Viewer', config.output_html_path, js_api=Api())
    
    # Start the webview
    webview.start(gui='qt', debug=True, http_port=8081)