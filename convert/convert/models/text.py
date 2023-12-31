from pydantic import BaseModel

from convert.models.common import S3Path


class TextRequest(BaseModel):
    input_text: S3Path
    output_pdf: S3Path
    output_tokens: S3Path
