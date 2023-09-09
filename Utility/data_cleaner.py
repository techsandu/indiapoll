class data_clear:
    def party_cleaner( input_String):
        common_cpim = ['cpi(m)', 'cpm', 'cpim']
        if input_String in common_cpim:
            return "CPI(M)"
        else:
            return input_String