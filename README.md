# pandoc-figure-caption-patch

Use with:

- [chart-filter](https://github.com/nihilor/pandoc-mermaid-chartjs-filter)
- [pandoc-plantuml](https://github.com/timofurrer/pandoc-plantuml-filter)
- [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/)

## Install 安装
```sh
pip install git+https://github.com/AClon314/pandoc-figure-caption-patch.git
```

> [!WARNING]
> Note the order of the filters/plugins, `pandoc-figure-caption-patch` comes **after** plugins for block-generated maps such as `pandoc-plantuml`, and `pandoc-crossref` has to come **last**.
> 
> 注意过滤器/插件的顺序，`pandoc-figure-caption-patch`在`pandoc-plantuml`等代码块生图的插件**之后**，`pandoc-crossref`必须在**最后**。
> ```yaml
> filters:
>   - chart-filter
>   - pandoc-plantuml
>   - pandoc-figure-caption-patch
>   - pandoc-crossref
> ```

## Usage 用法

~~~markdown
```mermaid
graph LR
A --> B
```
: mermaid's caption {#fig:mermaid}

```plantuml
A -> B
```
: uml's caption {#fig:uml}

~~~