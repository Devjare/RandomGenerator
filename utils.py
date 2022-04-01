from DistributionFactory import DistributionFactory
import plotly.express as px


def generate_pdf(distribution, sample_size, params):
    probabilities = []
    sample = []

    if distribution =='normal':
        try:
            distribution = DistributionFactory.get_distribution('normal', params)
            sample = distribution.get_sample(int(sample_size))
            for s in sample:
                probabilities.append(distribution.get_probability(s, False))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution =='binomial':
        try:
            distribution = DistributionFactory.get_distribution('binomial', params)
            sample = distribution.get_sample(int(sample_size))
            for s in sample:
                probabilities.append(distribution.get_probability(s, False))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution =='negbinomial':
        try:
            distribution = DistributionFactory.get_distribution('negativebinomial', params)
            sample = distribution.get_sample(int(sample_size))
            for s in sample:
                probabilities.append(distribution.get_probability(s, False))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution =='poisson':
        try:
            distribution = DistributionFactory.get_distribution('poisson', params)
            sample = distribution.get_sample(int(sample_size))
            #print("Sample: ",  sample)
            for s in sample:
                probabilities.append(distribution.get_probability(s, False))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution =='exponential':
        try:
            distribution = DistributionFactory.get_distribution('exponential', params)
            sample = distribution.get_sample(int(sample_size))
            for s in sample:
                probability = distribution.get_probability(s, False)
                #print('probability of %f: %f' % (s, probability))
                probabilities.append(probability)
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})

    #print("Sample: ", sample)
    #print("# # # # # # ########## probabilities ########### # # # # # # ", probabilities)
    fig = px.scatter(x=sample,y=probabilities)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def generate_plot(distribution, sample_size, params):
    x = []
    sample = []

    #print(params)

    if distribution == 'normal':
        try:
            distribution = DistributionFactory.get_distribution('normal', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})

    elif distribution == 'binomial':
        try:
            distribution = DistributionFactory.get_distribution('binomial', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})

    elif distribution == 'negbinomial':
        try:
            distribution = DistributionFactory.get_distribution('negativebinomial', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution == 'exponential':
        try:
            distribution = DistributionFactory.get_distribution('exponential', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    elif distribution == 'poisson':
        try:
            print("Poisson Args: ", params)
            distribution = DistributionFactory.get_distribution('poisson', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})

    for i in range(len(sample)):
        x.append(i)
    
    #print(sample)

    fig = px.scatter(x=x, y=sample)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig
