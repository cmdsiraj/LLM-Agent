from MyAgent.Tools.Tool import Tool
from MyAgent.utils.print_utils import log_tool_action
from pathlib import Path

class PdfHandlerTool(Tool):

    def __init__(self, show_tool_call: bool =True):
       
       self._name = "Pdf_handling_tool"
       self._description = (
        "Creates and saves a PDF file.\n"
        "Arguments: Requires 'html_content' in valid HTML format and 'output_filename' as the desired output file name.\n"
        "Notes: When using <img> tags, always include both width and height attributes to ensure images fit correctly in the PDF.\n"
        "Supports basic inline CSS styling. External scripts and JavaScript are not supported."
        )

       
       self.show_tool_call = show_tool_call
       
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    def _run_implementation(self, html_content: str, output_filename: str):
        from weasyprint import HTML

        try:
            if self.show_tool_call:
                log_tool_action("Executing PDF Handling Tool", "...", "🗃️", "blue")
            path = Path(f'output/{output_filename}')
            HTML(string=html_content).write_pdf(path)
            return f"Pdf {output_filename }created successfully (pdf content is also saved)"
        except Exception as e:
            return f"Got Exception while converting to pdf:\n{e}"
        