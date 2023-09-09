class query_handler:
    cand_select_query = "select candi_id from candidates where candi_name = %s and party_id = %s"
    new_cand_select_query = "select d.legit_id,d.legit_name,c.party_name as party,b.candi_id" \
                            " as id,b.candi_name as name,a.res_year as year,a.res_total as total " \
                            "from result_data as a inner join candidates as b on b.candi_id = a.res_candi_id " \
                            "inner join party as c on c.party_id = b.party_id " \
                            "inner join legit as d on d.legit_id = a.res_legit_id" \
                            " WHERE replace(replace(b.candi_name,' ',''),'.','') = %s and c.party_id = %s"