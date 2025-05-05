from flask import Flask, render_template, request
import matplotlib
# Set the backend to Agg (non-interactive) before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

def calculate_probabilities(sakit_positif, sakit_negatif, sehat_positif, sehat_negatif):
    # Calculate totalsh
    total_sakit = sakit_positif + sakit_negatif
    total_sehat = sehat_positif + sehat_negatif
    total_pasien = total_sakit + total_sehat
    
    # Calculate probabilities
    P_sakit = total_sakit / total_pasien
    P_sehat = total_sehat / total_pasien
    P_tes_positif_given_sakit = sakit_positif / total_sakit if total_sakit > 0 else 0
    P_tes_positif_given_sehat = sehat_positif / total_sehat if total_sehat > 0 else 0
    P_tes_positif = (P_tes_positif_given_sakit * P_sakit) + (P_tes_positif_given_sehat * P_sehat)
    P_sakit_given_tes_positif = (P_tes_positif_given_sakit * P_sakit) / P_tes_positif if P_tes_positif > 0 else 0
    
    return {
        'total_sakit': total_sakit,
        'total_sehat': total_sehat,
        'total_pasien': total_pasien,
        'P_sakit': P_sakit,
        'P_sehat': P_sehat,
        'P_tes_positif_given_sakit': P_tes_positif_given_sakit,
        'P_tes_positif_given_sehat': P_tes_positif_given_sehat,
        'P_tes_positif': P_tes_positif,
        'P_sakit_given_tes_positif': P_sakit_given_tes_positif,
        'sakit_positif': sakit_positif,
        'sakit_negatif': sakit_negatif,
        'sehat_positif': sehat_positif,
        'sehat_negatif': sehat_negatif
    }

def create_confusion_matrix_plot(data):
    plt.figure(figsize=(8, 6))
    matrix = [[data['sakit_positif'], data['sakit_negatif']],
              [data['sehat_positif'], data['sehat_negatif']]]
    
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Positif", "Negatif"],
                yticklabels=["Sakit", "Sehat"])
    plt.title('Confusion Matrix')
    
    # Save plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def create_bar_chart(data):
    plt.figure(figsize=(10, 6))
    categories = ['True Positive', 'False Positive', 'True Negative', 'False Negative']
    values = [data['sakit_positif'], data['sehat_positif'], 
              data['sakit_negatif'], data['sehat_negatif']]
    
    plt.bar(categories, values)
    plt.title('Distribusi Hasil Tes')
    plt.ylabel('Jumlah')
    
    # Save plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def create_pie_chart(data):
    plt.figure(figsize=(8, 8))
    labels = ['True Positive', 'False Positive', 'True Negative', 'False Negative']
    values = [data['sakit_positif'], data['sehat_positif'], 
              data['sakit_negatif'], data['sehat_negatif']]
    
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('Distribusi Hasil Tes')
    
    # Save plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def create_probability_tree(data):
    plt.figure(figsize=(12, 8))
    
    # Set up the plot
    plt.axis('off')
    
    # Define colors
    colors = {
        'sakit': '#FF9999',  # Light red
        'sehat': '#99FF99',  # Light green
        'positif': '#9999FF',  # Light blue
        'negatif': '#FFFF99',  # Light yellow
        'line': '#333333'  # Dark gray
    }
    
    # Draw the tree structure
    # Root node
    plt.plot([0.5, 0.5], [0.9, 0.7], color=colors['line'], linewidth=2)
    plt.text(0.5, 0.95, 'Total Pasien', ha='center', va='bottom', fontsize=12)
    
    # First level branches
    plt.plot([0.5, 0.25], [0.7, 0.5], color=colors['line'], linewidth=2)
    plt.plot([0.5, 0.75], [0.7, 0.5], color=colors['line'], linewidth=2)
    
    # Add boxes for first level nodes
    plt.gca().add_patch(plt.Rectangle((0.2, 0.45), 0.1, 0.2, facecolor=colors['sakit'], alpha=0.3, edgecolor=colors['line']))
    plt.gca().add_patch(plt.Rectangle((0.7, 0.45), 0.1, 0.2, facecolor=colors['sehat'], alpha=0.3, edgecolor=colors['line']))
    
    plt.text(0.25, 0.55, f'Sakit\n({data["total_sakit"]})', ha='center', va='top', fontsize=10)
    plt.text(0.75, 0.55, f'Sehat\n({data["total_sehat"]})', ha='center', va='top', fontsize=10)
    
    # Second level branches for Sakit
    plt.plot([0.25, 0.1], [0.5, 0.3], color=colors['line'], linewidth=2)
    plt.plot([0.25, 0.4], [0.5, 0.3], color=colors['line'], linewidth=2)
    
    # Add boxes for second level nodes (Sakit)
    plt.gca().add_patch(plt.Rectangle((0.05, 0.25), 0.1, 0.2, facecolor=colors['positif'], alpha=0.3, edgecolor=colors['line']))
    plt.gca().add_patch(plt.Rectangle((0.35, 0.25), 0.1, 0.2, facecolor=colors['negatif'], alpha=0.3, edgecolor=colors['line']))
    
    plt.text(0.1, 0.35, f'Positif\n({data["sakit_positif"]})', ha='center', va='top', fontsize=10)
    plt.text(0.4, 0.35, f'Negatif\n({data["sakit_negatif"]})', ha='center', va='top', fontsize=10)
    
    # Second level branches for Sehat
    plt.plot([0.75, 0.6], [0.5, 0.3], color=colors['line'], linewidth=2)
    plt.plot([0.75, 0.9], [0.5, 0.3], color=colors['line'], linewidth=2)
    
    # Add boxes for second level nodes (Sehat)
    plt.gca().add_patch(plt.Rectangle((0.55, 0.25), 0.1, 0.2, facecolor=colors['positif'], alpha=0.3, edgecolor=colors['line']))
    plt.gca().add_patch(plt.Rectangle((0.85, 0.25), 0.1, 0.2, facecolor=colors['negatif'], alpha=0.3, edgecolor=colors['line']))
    
    plt.text(0.6, 0.35, f'Positif\n({data["sehat_positif"]})', ha='center', va='top', fontsize=10)
    plt.text(0.9, 0.35, f'Negatif\n({data["sehat_negatif"]})', ha='center', va='top', fontsize=10)
    
    # Add probabilities with better formatting
    plt.text(0.25, 0.45, f'P = {data["P_sakit"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkred')
    plt.text(0.75, 0.45, f'P = {data["P_sehat"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkgreen')
    plt.text(0.1, 0.25, f'P = {data["P_tes_positif_given_sakit"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkblue')
    plt.text(0.4, 0.25, f'P = {1-data["P_tes_positif_given_sakit"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkblue')
    plt.text(0.6, 0.25, f'P = {data["P_tes_positif_given_sehat"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkblue')
    plt.text(0.9, 0.25, f'P = {1-data["P_tes_positif_given_sehat"]:.3f}', ha='center', va='bottom', fontsize=9, color='darkblue')
    
    # Add a legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor=colors['sakit'], alpha=0.3, edgecolor=colors['line'], label='Sakit'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors['sehat'], alpha=0.3, edgecolor=colors['line'], label='Sehat'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors['positif'], alpha=0.3, edgecolor=colors['line'], label='Positif'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors['negatif'], alpha=0.3, edgecolor=colors['line'], label='Negatif')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
    
    # Save plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input values
        sakit_positif = int(request.form['sakit_positif'])
        sakit_negatif = int(request.form['sakit_negatif'])
        sehat_positif = int(request.form['sehat_positif'])
        sehat_negatif = int(request.form['sehat_negatif'])
        
        # Calculate probabilities
        data = calculate_probabilities(sakit_positif, sakit_negatif, sehat_positif, sehat_negatif)
        
        # Create visualizations
        confusion_matrix = create_confusion_matrix_plot(data)
        bar_chart = create_bar_chart(data)
        pie_chart = create_pie_chart(data)
        probability_tree = create_probability_tree(data)
        
        return render_template('index.html', 
                             data=data,
                             confusion_matrix=confusion_matrix,
                             bar_chart=bar_chart,
                             pie_chart=pie_chart,
                             probability_tree=probability_tree)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)