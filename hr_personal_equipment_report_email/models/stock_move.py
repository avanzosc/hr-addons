# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import re
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def get_name_and_size(self):
        product_name = self.product_id.name
        product_name = re.sub(r'\s+', ' ', product_name.strip())
        
        product_lower = product_name.lower()
        if any(word in product_lower for word in ['zapatilla', 'bota', 'guante']):
            quant = 'PAR'
        else:
            quant = 'UD'
       
        size_indicators = ['TALLA', 'TAMAÑO', 'SIZE', 'MEDIDA']
      
        range_pattern = r'\b(XS|S|M|L|XL|2XL|3XL|4XL|5XL|XXL|XXXL)\s*-\s*(XS|S|M|L|XL|2XL|3XL|4XL|5XL|XXL|XXXL)\b'
        range_match = re.search(range_pattern, product_name, re.IGNORECASE)
        
        if range_match:
            full_range = range_match.group(0)
            name = product_name.replace(full_range, '').strip()
            return name, quant, full_range
    
        for indicator in size_indicators:
            pattern = r'\b' + re.escape(indicator) + r'\b'
            match = re.search(pattern, product_name, re.IGNORECASE)
            if match:
                parts = re.split(pattern, product_name, flags=re.IGNORECASE)
                if len(parts) > 1:
                    name = parts[0].strip()
                    size = parts[1].strip()
                    return name, quant, size
        
        words = product_name.split()
        
        if not words:
            return product_name, quant, None
        
        last_word = words[-1]
        second_last_word = words[-2] if len(words) >= 2 else ""
        
        size_patterns = [
            r'^(XS|S|M|L|XL|2XL|3XL|4XL|5XL|XXL|XXXL)$',
            r'^\d{1,2}$',
            r'^\d+$'
        ]
        
        for pattern in size_patterns:
            if re.match(pattern, last_word, re.IGNORECASE):
                name = ' '.join(words[:-1]).strip()
                return name, quant, last_word
        
        range_pattern_simple = r'^(XS|S|M|L|XL|2XL|3XL|4XL|5XL|XXL|XXXL)\s*-\s*(XS|S|M|L|XL|2XL|3XL|4XL|5XL|XXL|XXXL)$'
        last_two_words = f"{second_last_word} {last_word}" if second_last_word else last_word
        if re.match(range_pattern_simple, last_two_words, re.IGNORECASE):
            name = ' '.join(words[:-2]).strip()
            return name, quant, last_two_words
        
        return product_name, quant, None
