from marshmallow import pre_load, pre_dump, post_dump, Schema, post_load, fields


class BaseSchema(Schema):
    __envelope_key__ = {'single': None, 'many': None}

    def get_envelope_key(self, many):
        key = self.__envelope_key__['many'] if many else self.__envelope_key__['single']
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        # print(f"pre_load_data_get={data}")
        key = self.get_envelope_key(many)

        try:
            return data[key]
        except KeyError as e:
            print("error format or from swagger-ui")
            return data
        except Exception as e:
            return data

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        # print(f"post_dump_data_get={data}")
        key = self.get_envelope_key(many)
        return {
            key: data
        }


class DeleteResponseSchema(Schema):
    success = fields.Boolean()

    def convert_response(self, data, **kwargs):
        pass


delete_response_schema = DeleteResponseSchema()
