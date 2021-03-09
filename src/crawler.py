"""
크롤러 메인 모듈
"""
import click
from modules.search_crawler import SearchCrawler
from modules.category_crawler import CategoryCrawler


@click.command()
@click.option(
	'--mode',
	type=click.Choice(['search', 'category']),
	default='search',
	show_default=True
)
@click.option(
	'--min-idx', 
	type=click.INT,
	help='최소 인덱스 페이지',
	default=1,
	show_default=True
)
@click.option(
	'--max-idx',
	type=click.INT,
	help='최대 인덱스 페이지',
	required=True
)
@click.option(
	'--keyword',
	type=click.STRING,
	help='search mode일 경우, 입력되어야 함.',
	default="<None>",
	show_default=True
)
@click.option(
	'--order',
	type=click.Choice(['sim']),
	help='search mode일 경우, 검색 결과 순서 결정.',
	default='sim',
	show_default=True
)
@click.option(
	'--driver-version',
	help='크롬드라이버 버전 입력.',
	type=click.INT,
	default=89,
	show_default=True
)
@click.option(
	'--output',
	help='출력할 파일 경로.',
	type=click.STRING,
	required=True
)
def main(
	mode, min_idx, max_idx, 
	keyword, order, driver_version, output
):
	if mode == 'search':
		if keyword == '<None>':
			raise RuntimeError('keyword가 입력되지 않음.')
		crawler = SearchCrawler(
			keyword, 
			min_idx, 
			max_idx, 
			order, 
			driver_version, 
			output
		)
		crawler.process()

	elif mode == 'category':
		crawler = CategoryCrawler(
			min_idx,
			max_idx,
			driver_version,
			output
		)
		crawler.process()



if __name__ == '__main__':
	main()
