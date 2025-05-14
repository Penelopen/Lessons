#!/bin/bash
(	printf 'Отчет о логе веб-сервера\n========================\n'
	BASEDIR=`dirname $0`
	
	# Общее количество запросов
	total_cnt=0
	while read -r line; do
    	total_cnt=$((total_cnt + 1))
	done < $BASEDIR/access.log
	echo 'Общее количество запросов:' $total_cnt
	
	# Количество уникальных IP-адресов
	awk '{ ips[$1] = 1 } END { 
    	uniqe_count=0; 
    	for (i in ips) uniqe_count++; 
    	print "Количество уникальных IP-адресов:", uniqe_count 
	}' $BASEDIR/access.log
	
	echo ''
	
	# Количество запросов по методам (GET, POST и т.д.)
	echo "Количество запросов по методам:"
	awk '{
    	match($0, /"([A-Z]+) /)
    	method = substr($0, RSTART+1, RLENGTH-2)
    	methods[method]++
	} END {
    	for (m in methods) {
        	print "\t", methods[m], m
    	}
	}' $BASEDIR/access.log | sort -nr
	
	echo ''
	
	# Найти самый популярный URL (криво, но без gawk только так. Ведь у нас строго с awk)
	awk '{
    	if (match($0, /"[^ ]+ ([^ ]+) HTTP/)) {
    		sub(/.*"[^ ]+ /, "")
    		sub(/ .*$/, "")
        	urls[$0]++
    	}
	} END {
    	max_count = 0
    	for (u in urls) {
        	if (urls[u] > max_count) {
            	max_count = urls[u]
            	popular_url = u
        	}
    	}
    	print "Самый популярный URL:", max_count, popular_url
	}' $BASEDIR/access.log
) > report.txt
echo "Отчет сохранен в файл report.txt"
