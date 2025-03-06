output_path = os.path.join(current_dir,'Forced Convection Calculations.xlsx')
# with pd.ExcelWriter(output_path) as writer:
# 	measured_data.to_excel(writer, sheet_name='Calculations', index=False)
# with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
# 	measured_data.to_excel(writer, sheet_name='Calculations', index=False)
# 	workbook  = writer.book
# 	worksheet = writer.sheets['Calculations']
# 	for column in measured_data:
# 		column_width = max(measured_data[column].astype(str).map(len).max(), len(column))
# 		col_idx = measured_data.columns.get_loc(column)
# 		worksheet.set_column(col_idx, col_idx, column_width)
# os.startfile(output_path)

# plt.show()