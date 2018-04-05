#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <fstream>

using namespace std;

struct Answers
{
	size_t questionNo;
	int noAnswers;
	string answer;

	Answers()
	{
		questionNo = -1;
		noAnswers = 1;
		answer = "Brak";
	}

	Answers(const string& answer)
	{
		questionNo = -1;
		noAnswers = 1;
		this->answer = answer;
	}

	Answers(const size_t questionNo, const string& answer)
	{
		this->questionNo = questionNo;
		noAnswers = 1;
		this->answer = answer;
	}

	bool operator==(const Answers& other)
	{
		if(questionNo != other.questionNo)
		{
			return false;
		}
		else
		{
			return answer == other.answer;
		}
	}
};

bool compareAnswers(const Answers& l, const Answers& r)
{
	return l.noAnswers > r.noAnswers;
}

class Survey;
class Respondent
{
	friend class Survey;
	map<size_t, vector<string>> answers;

public:
	void addAnswer(const size_t& questionNo, const string& answer)
	{
		answers[questionNo].push_back(answer);
	}

	bool answerExist(const size_t& questionNo, const string& answer)
	{
		auto it = answers.find(questionNo);
		if(it != answers.end())
		{
			for(auto ans : it->second)
			{
				if(ans == answer)
				{
					return true;
				}
			}
		}
		return false;
	}

	ostream& displayAnswers(ostream& os)
	{
		for(auto answerSet : answers)
		{
			for(auto answer : answerSet.second)
			{
				os << answerSet.first << " " << answer << "\n";
			}
		}
		return os;
	}
};

class Correlation
{
	Answers mainAnswer;
	map<size_t, vector<Answers>> answers;
	friend bool compareCorrelation(const Correlation& l, const Correlation& r);

public:
	Correlation(const size_t& questionNo, const string& answer)
	: mainAnswer(questionNo, answer)
	{
		mainAnswer.noAnswers = 0;
	}

	void addAnswer(const size_t& questionNo, const string& answer)
	{
		if(mainAnswer == Answers(questionNo, answer))
		{
			mainAnswer.noAnswers++;
		}
		else
		{
			auto answerSet = answers.find(questionNo);
			if(answerSet != answers.end())
			{
				auto ans = find(answerSet->second.begin(), answerSet->second.end(), Answers(questionNo, answer));
				if(ans != answerSet->second.end())
				{
					ans->noAnswers++;
				}
				else
				{
					answers[questionNo].push_back(Answers(questionNo, answer));
				}
			}
			else
			{
				answers[questionNo].push_back(Answers(questionNo, answer));
			}
		}
	}

	ostream& display(ostream& os)
	{
		os << "Main Answer: " << mainAnswer.questionNo << ". " << mainAnswer.answer << " " << mainAnswer.noAnswers << "x\n";
		for(auto it : answers)
		{
			for(auto answer : it.second)
			{
				if(static_cast<double>(answer.noAnswers) / mainAnswer.noAnswers * 100 > 20)
				{
					os << "Answer: " << answer.questionNo << ". " << static_cast<double>(answer.noAnswers) / mainAnswer.noAnswers * 100 << "% " << answer.answer << " " << answer.noAnswers << "x\n";
				}
			}
		}
		return os;
	}

	void sort()
	{
		for(auto it : answers)
		{
			::sort(it.second.begin(), it.second.end(), compareAnswers);
		}
	}

	Answers getMainAnswer()
	{
		return mainAnswer;
	}

	map<size_t, vector<Answers>> getAnswers()
	{
		return answers;
	}
};

bool compareCorrelation(const Correlation& l, const Correlation& r)
{
	return l.mainAnswer.noAnswers > r.mainAnswer.noAnswers;
}

class Survey
{
	vector<string> questions;
	vector<Respondent> respondents;

public:
	ostream& displayQuestions(ostream& os)
	{
		for(auto question : questions)
		{
			os << question << "\n";
		}
		return os;
	}

	ostream& displayRespondents(ostream& os)
	{
		for(auto respondent : respondents)
		{
			respondent.displayAnswers(os);
			os << "\n";
		}
		return os;
	}

	ostream& displayCorrelations(ostream& os)
	{
		auto correlations = getCorrelations();
		for(auto correlation : correlations)
		{
			correlation.display(os);
			os << "\n";
		}
		return os;
	}

	void addQuestion(const string& question)
	{
		questions.push_back(question);
	}

	void addRespondent(const Respondent& respondent)
	{
		respondents.push_back(respondent);
	}

	void importCSV(const string& fileName)
	{
		string fullFileName = fileName;

		if(fullFileName.empty())
		{
			throw -1;
		}

		if(fullFileName.size() < 4 || fullFileName.substr(fullFileName.size() - 4, 4) != ".csv")
		{
			fullFileName += ".csv";
		}
		fstream file;
		file.open(fullFileName, fstream::in);

		string s;
		getline(file,s);
		s.erase(0, s.find(',') + 2);
		for(size_t pos = s.find('\"'); pos != string::npos; pos = s.find('\"'))
		{
			addQuestion(s.substr(0, pos));
			s.erase(0, pos + 1);
			if(!s.empty())
			{
				s.erase(0, 2);
			}
		}

		while(getline(file, s))
		{
			s.erase(0, s.find(',') + 2);
			Respondent r;
			size_t i = 1;
			for(size_t pos = s.find('\"'); pos != string::npos; pos = s.find('\"'), ++i)
			{
				string temp = s.substr(0, pos);
				for(size_t pos2 = temp.find(';'); pos2 != string::npos; pos2 = temp.find(';'))
				{
					r.addAnswer(i, temp.substr(0, pos2));
					temp.erase(0, pos2 + 1);
				}
				r.addAnswer(i, temp);
				s.erase(0, pos + 1);
				if(!s.empty())
				{
					s.erase(0, 2);
				}
			}
			addRespondent(r);
		}

		file.close();
	}

	void exportCSV(const string& fileName)
	{
		string fullFileName = fileName;

		if(fullFileName.empty())
		{
			throw -1;
		}

		if(fullFileName.size() < 4 || fullFileName.substr(fullFileName.size() - 4, 4) != ".csv")
		{
			fullFileName += ".csv";
		}
		fstream file;
		file.open(fullFileName, fstream::out | fstream::trunc);
		file << "Question Number,Question\n";

		for(size_t i = 0; i < questions.size(); ++i)
		{
			file << i + 1 << ",\"" << questions[i] << "\"\n";
		}
		file << "\n,Answer\n";

		file << "\n,Percentage,Answer,Number of Occurrences\n";
		vector<Correlation> correlations = getCorrelations();

		for(auto correlation : correlations)
		{
		    if(correlation.getMainAnswer().noAnswers != 1)
		    {
			Correlation temp = correlation;
			file << temp.getMainAnswer().questionNo << ",Topic,\"" << temp.getMainAnswer().answer << "\"," << temp.getMainAnswer().noAnswers << "\n";

			for(auto answers : temp.getAnswers())
			{
				for(auto answer : answers.second)
				{
					if(static_cast<double> (answer.noAnswers) / correlation.getMainAnswer().noAnswers * 100 >= 1)
					{
						file << answer.questionNo << "," << static_cast<double> (answer.noAnswers) / correlation.getMainAnswer().noAnswers * 100 << "%,\"" << answer.answer << "\"," << answer.noAnswers << "\n";
					}
				}
			}
			file << "\n";
		    }
		}
		file.close();
	}

	bool checkedAnswer(const size_t questionNo,
						const string& answer,
						const map<size_t, vector<string>>& checkedAnswers)
	{
		auto it = checkedAnswers.find(questionNo);
		if(it != checkedAnswers.end())
		{
			for(auto ans : it->second)
			{
				if(ans == answer)
				{
					return true;
				}
			}
		}
		return false;
	}
	vector<Correlation> getCorrelations()
	{
		vector<Correlation> correlations;
		map<size_t, vector<string>> checkedAnswers;

		for(size_t i = 1; i <= questions.size(); ++i)
		{
			for(size_t j = 0; j < respondents.size(); ++j)
			{
				for(size_t k = 0; k < respondents[j].answers[i].size(); ++k)
				{
					if(checkedAnswer(i, respondents[j].answers[i][k], checkedAnswers))
					{
						continue;
					}
					Correlation temp(i, respondents[j].answers[i][k]);

					for(size_t m = 0; m < respondents.size(); ++m)
					{
						if(respondents[m].answerExist(i, respondents[j].answers[i][k]))
						{
							for(size_t l = 1; l <= questions.size(); ++l)
							{
								for(size_t n = 0; n < respondents[m].answers[l].size(); ++n)
								{
									temp.addAnswer(l, respondents[m].answers[l][n]);
								}
							}
						}
					}
					checkedAnswers[i].push_back(respondents[j].answers[i][k]);
					correlations.push_back(temp);
				}
			}
		}
		return correlations;
	}
};

int main()
{
	cout << "Wersja Programu: 0.4\n";
	cout << "Autor: Anonimowy (Widziales getCorrelations i exportCSV?)\n\n";

	Survey survey;
	survey.importCSV("Ankieta");
	survey.exportCSV("Korelacje");

	survey.displayCorrelations(cout);
	return 0;
}
