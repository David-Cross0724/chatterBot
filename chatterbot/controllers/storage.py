from chatterbot.utils.module_loading import import_module


class StorageController(object):

    def __init__(self, adapter):
        self.storage_adapter = adapter

        self.recent_statements = []

    def get_last_statement(self):
        """
        Returns the last statement that was issued to the chat bot.
        If there was no last statement then return None.
        """
        if len(self.recent_statements) == 0:
            return None

        return self.recent_statements[-1]

    def get_responses(self, statement):
        """
        Returns the list of responses for a given statement.
        """
        return statement.get("in_response_to", [])

    def save_statement(self, **kwargs):
        """
        Update the database with the changes
        for a new or existing statement.
        """
        statement = list(kwargs.keys())[0]
        values = kwargs[statement]

        self.storage_adapter.update(statement, **values)

    def list_statements(self):
        """
        Returns a list of the statement text for all statements in the database.
        """
        # TODO: Call to _keys is bad
        return self.storage_adapter._keys()

    def get_statements_in_response_to(self, input_statement):
        """
        Returns a list of statement objects that are
        in response to a specified statement object.
        """
        statements = self.list_statements()
        results = []

        for statement in statements:

            result = self.storage_adapter.find(statement)

            if input_statement in self.get_responses(result.text):
                results.append(statement)

        return results

    def get_most_frequent_response(self, closest_statement):
        """
        Returns the statement with the greatest number of occurrences.
        """
        response_list = self.get_statements_in_response_to(closest_statement)

        # Initialize the matching responce to the closest statement.
        # This will be returned in the case that no match can be found.
        matching_response = closest_statement

        # The statement passed in must be an existing statement within the database
        statement_data = self.storage_adapter.find(matching_response)

        occurrence_count = statement_data.get_occurrence_count()

        for statement in response_list:

            statement_data = self.storage_adapter.find(statement)

            statement_occurrence_count = statement_data.get_occurrence_count()

            # Keep the more common statement
            if statement_occurrence_count >= occurrence_count:
                matching_response = statement
                occurrence_count = statement_occurrence_count

            #TODO? If the two statements occure equaly in frequency, should we keep one at random

        # Choose the most commonly occuring matching response
        return matching_response

