package main

import (
	"fmt"
	"regexp"
)

func main() {
	fmt.Println("START")
	var target_arr []string
	count_map := make(map[string]int)

	var str_arr []string
	str_arr = append(str_arr, `The Chinese national flag at the Memorial Hall in Nanjing is lowered to half mast on Thursday to commemorate the more than 300,000 people who were killed by Japanese invaders in the <a href="/hashtag/NanjingMassacre?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>NanjingMassacre</b></a> starting on December 13, 1937. <a href="/hashtag/NationalMemorialDay?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>NationalMemorialDay</b></a><a href="https://t.co/S8r9Zo1kSg" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/S8r9Zo1kSg</a> <a href="/hashtag/RenewableEnergy?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>RenewableEnergy</b></a> will take up more than 10% of Beijing Daxing International Airport&#39;s energy consumption mix when completed next year, the <a href="/hashtag/highest?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>highest</b></a> among all airports in the country, said the municipal authorities on late Wednesday<a href="https://t.co/TTHKjpwDIZ" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/TTHKjpwDIZ</a> Aerial photos taken on Dec. 12, 2018, show winter <a href="/hashtag/rime?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>rime</b></a> scenery on the bank of the Songhua River in Jilin City, northeast China&#39;s Jilin Province. (Photo/Xinhua)<a href="https://t.co/p55bauA2U0" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/p55bauA2U0</a>`)
	str_arr = append(str_arr, `The Chinese national flag at the Memorial Hall in Nanjing is lowered to half mast on Thursday to commemorate the more than 300,000 people who were killed by Japanese invaders in the <a href="/hashtag/NanjingMassacre?src=hash" data-query-source="hashtag_click"<s>#</s><b>Res123123newableEnergy</b> class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>NanjingMassacre</b></a> starting on December 13, 1937. <a href="/hashtag/NationalMemorialDay?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>NationalMemorialDay</b></a><a href="https://t.co/S8r9Zo1kSg" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/S8r9Zo1kSg</a> <a href="/hashtag/RenewableEnergy?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>RenewableEnergy</b></a> will take up more than 10% of Beijing Daxing International Airport&#39;s energy consumption mix when completed next year, the <a href="/hashtag/highest?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><b>highest</b></a> among all airports in the country, said the municipal authorities on late Wednesday<a href="https://t.co/TTHKjpwDIZ" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/TTHKjpwDIZ</a> Aerial photos taken on Dec. 12, 2018, show winter <a href="/hashtag/rime?src=hash" data-query-source="hashtag_click" class="twitter-hashtag pretty-link js-nav" dir="ltr" ><s>#</s><brime</b></a> scenery on the bank of the Songhua River in Jilin City, northeast China&#39;s Jilin Province. (Photo/Xinhua)<a href="https://t.co/p55bauA2U0" class="twitter-timeline-link u-hidden" data-pre-embedded="true" dir="ltr" >pic.twitter.com/p55bauA2U0</a>`)
	reg := regexp.MustCompile(`<s>.</s><b>(\w*)</b>`)

	fmt.Println("---------------------------------------")
//	fmt.Println("res:", reg.FindAllString(str, -1))
	fmt.Println("---------------------------------------")
	for _, str := range str_arr {
		fmt.Println("res Sub:", reg.FindAllStringSubmatch(str, -1))
		for _, find_arr := range reg.FindAllStringSubmatch(str, -1) {
			target_str := find_arr[1]
			_, ok := count_map[target_str]
			if !ok {
				target_arr = append(target_arr, target_str)
				count_map[target_str] = 1
				continue
			}
			count_map[target_str] += 1
		}
	}
	fmt.Println("target_arr:", target_arr)
	fmt.Println("count_map:", count_map)

	fmt.Println("END")
}
