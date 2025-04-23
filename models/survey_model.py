import pandas as pd

class SurveyModel:
    def __init__(self):
        self.df = None

    def load_csv(self, file_path):
        """Carga los datos desde un archivo CSV"""
        self.df = pd.read_csv(file_path)
        return True

    def get_summary(self):
        """Genera un resumen de los datos"""
        if self.df is None:
            return ""
        
        resumen = ""
        for col in self.df.columns:
            resumen += f"== Pregunta: {col} ==\n"
            counts = self.df[col].value_counts(dropna=False)
            for val, cnt in counts.items():
                resumen += f"  • {val}: {cnt}\n"
            resumen += "\n"
        return resumen

    def get_column_data(self, column):
        """Obtiene los datos de una columna específica"""
        if self.df is None or column not in self.df.columns:
            return None
        return self.df[column].value_counts(dropna=False)

    def get_columns(self):
        """Retorna la lista de columnas disponibles"""
        return list(self.df.columns) if self.df is not None else []

    def has_data(self):
        """Verifica si hay datos cargados"""
        return self.df is not None
