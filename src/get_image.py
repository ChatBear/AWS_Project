def create_presigned_url(s3_client, object_name, expiration=3600, bucket_name="projecttolondon"):
    url_signed = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    
    return url_signed


