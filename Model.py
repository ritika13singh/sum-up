from transformers import PegasusTokenizer
import pickle
import torch

model_name = 'google/pegasus-wikihow'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer_sum = PegasusTokenizer.from_pretrained(model_name)
path = open("C:\\Users\\saksh\\Downloads\\model_summ", 'rb')
model_sum = pickle.load(path)
src_text = "This paper is the introduction to the special issue entitled: ‘Governing artificial intelligence: ethical, legal and technical opportunities and challenges'. Artificial intelligence (AI) increasingly permeates every aspect of our society, from the critical, like urban infrastructure, law enforcement, banking, healthcare and humanitarian aid, to the mundane like dating. AI, including embodied AI in robotics and techniques like machine learning, can improve economic, social welfare and the exercise of human rights. Owing to the proliferation of AI in high-risk areas, the pressure is mounting to design and govern AI to be accountable, fair and transparent. How can this be achieved and through which frameworks? This is one of the central questions addressed in this special issue, in which eight authors present in-depth analyses of the ethical, legal-regulatory and technical challenges posed by developing governance regimes for AI systems. It also gives a brief overview of recent developments in AI governance, how much of the agenda for defining AI regulation, ethical frameworks and technical approaches is set, as well as providing some concrete suggestions to further the debate on AI governance."
batch = tokenizer_sum.prepare_seq2seq_batch(src_text, truncation=True, padding='longest', return_tensors="pt").to(torch_device)
translated = model_sum.generate(**batch)
tgt_text = tokenizer_sum.batch_decode(translated, skip_special_tokens=True)