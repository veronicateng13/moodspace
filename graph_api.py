import json
import plotly
import plotly.graph_objects as go

class CreateGraph:
    # provide values for attribute name @ runtime        
    def get_line_graph(self, month_df):
        # create figure
        line_fig = go.Figure()
        month_ls = list(month_df.month)
        thread_ls = list(month_df.number_of_threads)

        # add trace
        line_fig.add_trace(go.Scatter(
            x = month_ls, y = thread_ls,
            mode = "lines+text",
            text = thread_ls, textposition = "top center"
        ))

        # set title
        line_fig.update_layout( title_text=f"Number of Threads over a Period of Time (Overall)", height=550)

        # set x label: show only relevant months
        line_fig.layout.xaxis.tickvals = month_ls
        line_fig.layout.xaxis.tickformat = '%b %Y'

        # range selector
        buttons=list([ dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=12, label="1Y", step="month", stepmode="backward"),
                        dict(count=36, label="3Y", step="month", stepmode="backward"),
                        dict(label="All", step="all") ])

        line_fig.update_layout(
            xaxis = dict(tickformat = "%b %Y",
                            rangeselector = dict(buttons = buttons),
                                            rangeslider = dict(visible = True),
                                            type = "date"
                    )
        )
        graphJSON = json.dumps(line_fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
    def get_bar_graph(self, pred_df):
        # BAR CHART: using pred_df
        # add label col
        col = ['category', 'clean_text']
        overall_df = pred_df[col].groupby('category').count()
        overall_df.loc[:,'percentage'] = (overall_df['clean_text']/overall_df['clean_text'].sum() * 100).astype(int)
        overall_df['percentage'] = overall_df['percentage'].astype(str) + '%'
        overall_df['chart_label'] = overall_df['clean_text'].astype(str) + "  (" + overall_df['percentage'] + ")"

        # add trace
        bar_fig = go.Figure(data = [go.Bar(
                                x = list(overall_df.index.values), y = overall_df['clean_text'],
                                text = overall_df['chart_label'],
                                textposition = 'inside'
        )])
        bar_fig.update_layout(title=f"Number of Threads by Category")
        bar_fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
        
        graphJSON = json.dumps(bar_fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
    def get_stacked_bar_graph(self, month_cat_df):
        # set figure
        stackbar_fig = go.Figure()

        #
        neg_df = month_cat_df[month_cat_df.category == 'Negative']
        not_neg_df = month_cat_df[month_cat_df.category == 'Not Negative']

        # add bars
        stackbar_fig.add_bar(name = 'Not Negative', 
                    x=list(not_neg_df.month), y=list(not_neg_df.number_of_threads),
                    text = list(not_neg_df.number_of_threads))

        stackbar_fig.add_bar(name = 'Negative', 
                    x=list(neg_df.month), y=list(neg_df.number_of_threads),
                    text = list(neg_df.number_of_threads))

        # set x label
        stackbar_fig.layout.xaxis.tickvals = list(month_cat_df.month)
        stackbar_fig.layout.xaxis.tickformat = '%b %Y'

        # set bar mode
        stackbar_fig.update_layout(barmode="relative")

        # set title
        stackbar_fig.update_layout( title_text=f"Number of Threads over a Period of Time (Comparison)")
        
        graphJSON = json.dumps(stackbar_fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON