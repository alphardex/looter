import pandas as pd
from jieba.analyse import extract_tags
data = pd.read_json('zhilian_details.json', encoding='utf-8')
buxian = len(data[data.degree == '不限'])
gaozhong = len(data[data.degree == '高中'])
zhongji = len(data[data.degree == '中技'])
zhongzhuan = len(data[data.degree == '中专'])
dazhuan = len(data[data.degree == '大专'])
benke = len(data[data.degree == '本科'])
shuoshi = len(data[data.degree == '硕士'])
boshi = len(data[data.degree == '博士'])
print(f'职位要求:\n不限：{buxian}\n高中：{gaozhong}\n中技：{zhongji}\n中专：{zhongzhuan}\n大专：{dazhuan}\n本科：{benke}\n硕士：{shuoshi}\n博士：{boshi}')
details = data.detail
details = ' '.join(list(details))
tags = extract_tags(details, topK=300, withWeight=False)
text = " ".join(tags)
for i, tag in enumerate(tags):
    print(f'{i}. {tag}')