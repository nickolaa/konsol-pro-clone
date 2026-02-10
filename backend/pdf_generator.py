from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile


class PDFGenerator:
    """Генератор PDF документов"""
    
    def __init__(self):
        self.buffer = BytesIO()
        self.canvas = None
    
    def generate_contract(self, contract):
        """Генерирует PDF договора"""
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        width, height = A4
        
        # Заголовок
        self.canvas.setFont('Helvetica-Bold', 16)
        self.canvas.drawCentredString(width / 2, height - 2*cm, 
                                     f'ДОГОВОР №{contract.contract_number}')
        
        # Дата
        self.canvas.setFont('Helvetica', 12)
        self.canvas.drawString(2*cm, height - 3*cm, 
                              f'от {contract.contract_date.strftime("%d.%m.%Y")}')
        
        y = height - 5*cm
        
        # Стороны договора
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, 'Заказчик:')
        y -= 0.7*cm
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, f'{contract.employer.telegram_id or contract.employer.phone}')
        
        y -= 1.5*cm
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, 'Исполнитель:')
        y -= 0.7*cm
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, f'{contract.freelancer.telegram_id or contract.freelancer.phone}')
        
        # Предмет договора
        y -= 2*cm
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, '1. ПРЕДМЕТ ДОГОВОРА')
        
        y -= 1*cm
        self.canvas.setFont('Helvetica', 11)
        # Разбиваем текст на строки
        text = f'Исполнитель обязуется выполнить следующие работы: {contract.work_description}'
        self._draw_multiline_text(text, 2*cm, y, width - 4*cm)
        
        # Стоимость и сроки
        y -= 3*cm
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, '2. СТОИМОСТЬ И СРОКИ')
        
        y -= 1*cm
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, f'Стоимость работ: {contract.amount} руб.')
        y -= 0.7*cm
        self.canvas.drawString(2*cm, y, f'Срок выполнения: {contract.deadline.strftime("%d.%m.%Y")}')
        
        # Подписи
        y = 5*cm
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, '_' * 30)
        self.canvas.drawString(2*cm, y - 0.7*cm, 'Заказчик')
        
        self.canvas.drawString(width - 10*cm, y, '_' * 30)
        self.canvas.drawString(width - 10*cm, y - 0.7*cm, 'Исполнитель')
        
        self.canvas.save()
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return ContentFile(pdf, name=f'contract_{contract.contract_number}.pdf')
    
    def generate_act(self, act):
        """Генерирует PDF акта"""
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        width, height = A4
        
        # Заголовок
        self.canvas.setFont('Helvetica-Bold', 16)
        self.canvas.drawCentredString(width / 2, height - 2*cm, 
                                     f'АКТ №{act.act_number}')
        
        self.canvas.setFont('Helvetica', 12)
        self.canvas.drawCentredString(width / 2, height - 2.7*cm, 
                                     'приемки-передачи выполненных работ')
        
        # Дата
        self.canvas.drawString(2*cm, height - 4*cm, 
                              f'от {act.act_date.strftime("%d.%m.%Y")}')
        
        y = height - 5.5*cm
        
        # К договору
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, f'к Договору №{act.contract.contract_number}')
        
        # Выполненные работы
        y -= 2*cm
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, 'ВЫПОЛНЕННЫЕ РАБОТЫ')
        
        y -= 1*cm
        self.canvas.setFont('Helvetica', 11)
        text = act.work_performed
        self._draw_multiline_text(text, 2*cm, y, width - 4*cm)
        
        # Стоимость
        y -= 3*cm
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(2*cm, y, f'ИТОГО: {act.amount} руб.')
        
        # Подписи
        y = 5*cm
        self.canvas.setFont('Helvetica', 11)
        self.canvas.drawString(2*cm, y, '_' * 30)
        self.canvas.drawString(2*cm, y - 0.7*cm, 'Заказчик')
        
        self.canvas.drawString(width - 10*cm, y, '_' * 30)
        self.canvas.drawString(width - 10*cm, y - 0.7*cm, 'Исполнитель')
        
        self.canvas.save()
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return ContentFile(pdf, name=f'act_{act.act_number}.pdf')
    
    def _draw_multiline_text(self, text, x, y, max_width):
        """Вспомогательный метод для разбиения текста на строки"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.canvas.stringWidth(test_line, 'Helvetica', 11) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines:
            self.canvas.drawString(x, y, line)
            y -= 0.6*cm
        
        return y
