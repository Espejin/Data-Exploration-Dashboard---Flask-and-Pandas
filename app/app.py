from flask import Flask, render_template, request, url_for, redirect
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import sqlite3
import pandas as pd

import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)


# Función querys a db:
def sql_to_df(bdd, query):
    # Conectar a la base de datos
    conn = sqlite3.connect(bdd)
    
    # Leer datos de la base de datos en un DataFrame de pandas
    df = pd.read_sql_query(query, conn)
    
    # Cerrar la conexión
    conn.close()
    
    return df

#Función fig del plot a img_base64
def fig_to_img(fig):

     # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)  # Cerrar el gráfico para liberar memoria

    # Convertir la imagen a base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')

    return img_base64 

def return_dim(tb_name, tb_column):
    
    query =  "SELECT DISTINCT " + tb_column + " FROM " + tb_name + " ORDER BY 1 ASC"
    df_dev = sql_to_df('developers_data.db', query)
    df_dev = df_dev[tb_column].tolist()
    df_dev.insert(0,'All')
    return df_dev

def generate_where(age,oss):
    
    wh_query = "WHERE "

    if age not in ('','All'):
        wh_query = wh_query + " A.Age = '" + age +"' "
        if oss not in ('','All'):
            wh_query = wh_query + " AND A.ResponseId IN (SELECT ResponseId FROM Os_Prof_Use WHERE OsProfUse = '" + oss +"') "
    elif age in ('','All') and oss not in ('','All'):
        wh_query = wh_query + " A.ResponseId IN (SELECT ResponseId  FROM Os_Prof_Use WHERE OsProfUse = '" + oss +"') "
    else:
        wh_query = ""
    
    return wh_query


def extract_first_two_words(text):
    words = text.split()  # Dividir el texto en palabras
    return ' '.join(words[:2])

#Grafico sección 1
def graf_bar_1(filt_age,filt_ops):

    sql_query = "SELECT DevType, AVG(AnnualSalary) AS AnnualSalary FROM (SELECT DevType, AVG(ConvertedCompYearly) AS AnnualSalary, COUNT(1) AS CONT FROM User_Info A "+ generate_where(filt_age,filt_ops) +" GROUP BY  DevType ORDER BY 3 DESC LIMIT 10) A GROUP BY DevType ORDER BY 2 DESC LIMIT 6"
    #Exportar SQL y cambiar tipo de dato:
    df_dev = sql_to_df('developers_data.db',sql_query)
    df_dev['AnnualSalary'] = round(df_dev['AnnualSalary'].astype(float),2)
    df_dev['DevType'] = df_dev['DevType'].apply(extract_first_two_words) 
    df_dev = df_dev[df_dev['DevType'] != 'Other Developer']     

    #Imprimir Datos
    fig, ax = plt.subplots(figsize=(12,10))

    # Crear el gráfico de barras horizontal usando Seaborn y asignar el objeto de ejes
    sns.barplot(x='AnnualSalary', y='DevType', data=df_dev, orient='h', palette='viridis', ax=ax)


    # Configurar el título y etiquetas del gráfico
    ax.set_title('Annual Salary vs Developer Type', fontsize=18)
    ax.set_xlabel('')
    ax.set_ylabel('')

    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=15)


    plt.tight_layout()

    return fig_to_img(fig)

def graf_bar_2(filt_age,filt_ops):

    sql_query = "SELECT Country, AnualSalary  FROM (SELECT Country, AVG(ConvertedCompYearly) AS AnualSalary , COUNT(1) AS Count FROM User_Info A " + generate_where (filt_age,filt_ops) + " GROUP BY Country ORDER BY 3 DESC LIMIT 7) A ORDER BY AnualSalary DESC LIMIT 6"
    df_dev = sql_to_df('developers_data.db', sql_query)
    df_dev['AnualSalary'] = round(df_dev['AnualSalary'].astype(float),2)
    df_dev['Country'] = df_dev['Country'].apply(extract_first_two_words)

    # Crear la figura y el objeto de ejes
    fig, ax = plt.subplots(figsize=(12, 10))

    # Crear el gráfico de barras horizontal usando Seaborn y asignar el objeto de ejes
    sns.barplot(x='AnualSalary', y='Country', data=df_dev, orient='h',palette='viridis')

    # Configurar el título y etiquetas del gráfico
    ax.set_title('Annual Salary vs Country', fontsize=18)
    ax.set_xlabel('')
    ax.set_ylabel('')


    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=15)


    plt.tight_layout()

    return fig_to_img(fig)

def pie_chart_3(filt_age,filt_ops):

    sql_query = "SELECT WebFrameWork,Count(1) as Users FROM User_Info A INNER JOIN Web_Frame_Work B ON B.ResponseId = A.ResponseId " + generate_where(filt_age,filt_ops) +" GROUP BY WebFrameWork ORDER BY 2 DESC LIMIT 10"
    df_dev = sql_to_df('developers_data.db', sql_query)
    
    fig, ax = plt.subplots()
    
    ax.pie(df_dev['Users'], labels=df_dev['WebFrameWork'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))

    # Configurar el título y etiquetas del gráfico
    ax.set_title('Usage of Web Frameworks')


    return fig_to_img(fig)

def pie_chart_4(filt_age,filt_ops):
    
    sql_query = "SELECT BDDWork,Count(1) as Users FROM User_Info A INNER JOIN BDD_Work B ON B.ResponseId = A.ResponseId " + generate_where(filt_age,filt_ops) +" GROUP BY BDDWork ORDER BY 2 DESC LIMIT 10"
    df_dev = sql_to_df('developers_data.db', sql_query)
 
    fig, ax = plt.subplots()
    
    ax.pie(df_dev['Users'], labels=df_dev['BDDWork'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))

    # Configurar el título y etiquetas del gráfico
    ax.set_title('Usage of DBs')


    return fig_to_img(fig)


def disper_graf_5(filt_age, filt_ops):
    query_disp = """
        SELECT 
            WorkExp,
            ConvertedCompYearly AS AnnualSalary,
            CASE 
                WHEN A.Industry = 'Information Services, IT, Software Development, or other Technology' THEN 'IT & Development' 
                WHEN B.Industry IS NULL THEN 'Other'
                ELSE SUBSTR(A.Industry, 1, INSTR(A.Industry || ' ', ' ') - 1) 
            END AS Industry
        FROM User_Info A
        LEFT JOIN (
            SELECT Industry, COUNT(1) AS CONT 
            FROM User_Info 
            GROUP BY Industry 
            ORDER BY 2 DESC 
            LIMIT 6
        ) B ON B.Industry = A.Industry
    """

    rest_where_clause = " DevType NOT IN ('Other', 'Other Developer') AND A.Industry NOT IN ('Other') "
    
    if generate_where(filt_age, filt_ops) in ('All', ''):
        query_disp = query_disp + " WHERE " + rest_where_clause
    else:
        query_disp = query_disp + generate_where(filt_age, filt_ops) + " AND " + rest_where_clause
    
    df_dev = sql_to_df('developers_data.db', query_disp)
    df_dev['AnnualSalary'] = round(df_dev['AnnualSalary'].astype(float), 2)
    df_dev['WorkExp'] = df_dev['WorkExp'].astype(int)

    # Crear la figura y el objeto de ejes
    fig, ax = plt.subplots(figsize=(14, 12))

    sns.scatterplot(x='WorkExp', y='AnnualSalary', data=df_dev, hue='Industry')

    # Configurar el título y etiquetas del gráfico
    ax.set_title('Annual Salary vs WorkExp', fontsize=18)
    ax.set_xlabel('WorkExp', fontsize=14)
    ax.set_ylabel('Annual Salary', fontsize=14)
    ax.legend(title='Industry', title_fontsize='14', fontsize='14', loc='best')
    plt.ylim(0, 500000)

    return fig_to_img(fig)


def corr_graf_6(filt_age,filt_ops):

    sql_query = "SELECT  YearsCode, ConvertedCompYearly as AnnualSalary, YearsCodePro FROM User_Info A " + generate_where(filt_age,filt_ops)
    df_dev = sql_to_df('developers_data.db', sql_query)

    df_dev['AnnualSalary'] = round(df_dev['AnnualSalary'].astype(float),2)
    df_dev['YearsCode'] = df_dev['YearsCode'].astype(int)
    df_dev['YearsCodePro'] = df_dev['YearsCodePro'].astype(int)

    correlation_matrix = df_dev.corr()

    fig, ax = plt.subplots(figsize=(6, 6))  # Ajustar el tamaño de la figura

    sns.heatmap(correlation_matrix, 
                annot=True,                # Mostrar los valores en cada celda
                cmap='coolwarm',           # Paleta de colores
                fmt='.2f',                 # Formato de los valores
                linewidths=0.5,            # Ancho de las líneas que separan las celdas
                vmin=-1, vmax=1) 

    ax.set_title('Correlation of YearsCodePro, YearsCode, Annual Salary')

    return fig_to_img(fig)



def create_plot(plot_id,filt_age,filt_ops):
    # Configurar Matplotlib para cada gráfica

    if plot_id == 1:

        return graf_bar_1(filt_age,filt_ops)
    
    elif plot_id == 2:

        return graf_bar_2(filt_age,filt_ops)
    
    elif plot_id == 3:

        return pie_chart_3(filt_age,filt_ops)
    
    elif plot_id == 4:

        return pie_chart_4(filt_age,filt_ops)
    
    elif plot_id == 5:

        return disper_graf_5(filt_age,filt_ops)
    
    elif plot_id == 6:

        return corr_graf_6(filt_age,filt_ops)
     

    return img_base64


@app.route('/')
def index():

    sel_opt = request.args.get('sel_option', '')
    sel_opt_oss = request.args.get('sel_oss', '')
    plots = [create_plot(i,sel_opt,sel_opt_oss) for i in range(1, 7)]
    dim_age = return_dim('User_Info', 'Age')
    dim_oss = return_dim('OS_Prof_Use','OSProfUse')
    return render_template('index.html', plots=plots,ages=dim_age,oss=dim_oss,sel_option=sel_opt,sel_oss=sel_opt_oss)


@app.route('/submit', methods=['POST'])
def submit():
    
    sel_opt = request.form.get('opt_age')
    sel_opt_oss = request.form.get('opt_os')

    # Redirigir a la misma página o a otra página
    return redirect(url_for('index',sel_option=sel_opt,sel_oss=sel_opt_oss))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/process')
def process():
    return render_template('process.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)