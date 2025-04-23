from models.survey_model import SurveyModel
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class SurveyController:
    def __init__(self):
        self.model = SurveyModel()

    def load_csv(self, file_path):
        """Intenta cargar un archivo CSV"""
        try:
            return self.model.load_csv(file_path)
        except Exception as e:
            raise Exception(f"No se pudo cargar el CSV: {str(e)}")

    def get_summary(self):
        """Obtiene el resumen de los datos"""
        return self.model.get_summary()

    def get_columns(self):
        """Obtiene la lista de columnas disponibles"""
        return self.model.get_columns()

    def has_data(self):
        """Verifica si hay datos cargados"""
        return self.model.has_data()

    def generate_chart(self, column, chart_type):
        """Genera una gráfica basada en los datos de una columna"""
        counts = self.model.get_column_data(column)
        if counts is None:
            return None

        fig = Figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111)

        if chart_type == "pastel":
            wedges, texts, autotexts = ax.pie(
                counts.values,
                labels=counts.index,
                autopct='%1.1f%%',
                textprops={'color': '#000000', 'fontsize': 14, 'weight': 'bold'},
                pctdistance=0.85
            )
            ax.set_title(f"Distribución de {column}", color='#000000', pad=20, fontsize=16, weight='bold')
            
        elif chart_type == "barras":
            bars = ax.bar(range(len(counts)), counts.values)
            ax.set_title(f"Frecuencia de {column}", color='#000000', pad=20, fontsize=16, weight='bold')
            ax.set_xlabel("Respuestas", color='#000000', fontsize=14)
            ax.set_ylabel("Frecuencia", color='#000000', fontsize=14)
            
            ax.tick_params(axis='both', colors='#000000')
            ax.set_xticks(range(len(counts)))
            ax.set_xticklabels(counts.index, rotation=45, ha='right', fontsize=14)
            
            for i, bar in enumerate(bars):
                bar.set_color('#2196F3')
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', color='#000000', 
                       fontsize=14, weight='bold')

        fig.tight_layout()
        return fig

    def save_chart(self, fig, file_path):
        """Guarda la gráfica en un archivo"""
        try:
            fig.savefig(file_path, bbox_inches='tight')
            return True
        except Exception as e:
            raise Exception(f"No se pudo guardar la gráfica: {str(e)}")
