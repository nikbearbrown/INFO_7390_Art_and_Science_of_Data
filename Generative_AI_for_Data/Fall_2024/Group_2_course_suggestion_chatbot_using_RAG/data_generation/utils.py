def save_to_csv(df, output_path):
    """Saves a DataFrame to a CSV file."""
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")


def save_to_txt(content, output_path):
    """Saves text content to a file."""
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)
    print(f"Text saved to {output_path}")
