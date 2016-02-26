#! /usr/bin/env python

import sys
import boto
import boto.s3.connection
access_key = 'TVJ75XYZODLSWC66VNHX'
secret_key = 'rMjbDJj12FP7jshF9QMGyQHJDbcQlz8ps7Flffmp'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'ceph-rgw',
        is_secure=False,
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)

def help():
        print ""
        print sys.argv[0] + " command"
        print "----------------"
        print "list\t: Listing owned buckets & Listing a bucket's content"
        print "create\t: Creating a bucket"
        print "delete\t: Deleting a bucket"
        print "add\t: Creating an object"
        print "remove\t: Deleting an object"
        print "acl\t: Change an object's ACL"
        print "url\t: Generate object download URLs"
        print "help\t: Usages"

def chk_argv():
        if len(sys.argv) < 3:
                sys.exit(1)
        
def list():
        if len(sys.argv) < 3:
                print "Listing owned buckets"
                for bucket in conn.get_all_buckets():
                        print "{name}\t{created}".format(
                                name = bucket.name,
                                created = bucket.creation_date,
                        )
        else:
                print "Listing a bucket's content"
                bucket = conn.get_bucket(sys.argv[2])
                for key in bucket.list():
                        print "{name}\t{size}\t{modified}".format(
                                name = key.name,
                                size = key.size,
                                modified = key.last_modified,
                        )

def create():
        print "Creating a bucket"
        if len(sys.argv) < 3:
                print "Not enough parameters"
                print sys.argv[0],sys.argv[1],"BucketName"
                sys.exit(1)
        else:
                bucket = conn.create_bucket(sys.argv[2])

def delete():
        print "Deleting a bucket"
        if len(sys.argv) < 3:
                print "Not enough parameters"
                print sys.argv[0],sys.argv[1],"BucketName"
                sys.exit(1)
        else:
                conn.delete_bucket(sys.argv[2])

def add():
        print "Creating an object"
        if len(sys.argv) == 5:
                bucket = conn.create_bucket(sys.argv[2])
                file = sys.argv[3]
                object = sys.argv[4]
                key = bucket.new_key(object)
                key.set_contents_from_filename(file)
                hello_key = bucket.get_key(object)
                hello_key.set_canned_acl('public-read')
        else:
                print sys.argv[0],sys.argv[1],"Bucket_Name File ObjectName"
        
def remove():
        print "Deleting an object"
        if len(sys.argv) == 4:
                bucket = conn.get_bucket(sys.argv[2])
                object = sys.argv[3]
                bucket.delete_key(object)
        else:
                print sys.argv[0],sys.argv[1],"Bucket_Name ObjectName"

def acl():
	print "Change an object's ACL"
	if len(sys.argv) == 4:
		bucket = conn.get_bucket(sys.argv[2])
		acl_select = sys.argv[3]
		hello_key = bucket
	elif len(sys.argv) == 5:
		bucket = conn.get_bucket(sys.argv[2])
		acl_select = sys.argv[3]
		object = sys.argv[4]
		hello_key = bucket.get_key(object)
	else:
		print sys.argv[0],sys.argv[1],"Bucket_Name [pri|pub] ObjectName"
	if acl_select == 'pub':
		print "change to public-read"
		hello_key.set_canned_acl('public-read')
	elif acl_select == 'pri':
		print "change to private"
		hello_key.set_canned_acl('private')
	else:
		print "ACL no change"

def url():
        print "Generate object download URLs"
        if len(sys.argv) == 4:
                bucket = conn.get_bucket(sys.argv[2])
                object = sys.argv[3]
                hello_key = bucket.get_key(object)
                hello_url = hello_key.generate_url(0, query_auth=False, force_http=True)
                print hello_url
        elif len(sys.argv) == 5:
                bucket = conn.get_bucket(sys.argv[2])
                object = sys.argv[3]
                auth = sys.argv[4]
                if auth == 'signed':
                        hello_key = bucket.get_key(object)
                        hello_url = hello_key.generate_url(3600, query_auth=True, force_http=True)
                        print hello_url
                else:
                        print sys.argv[0],sys.argv[1],"Bucket_Name ObjectName [signed]"   
        else:
                print sys.argv[0],sys.argv[1],"Bucket_Name ObjectName [signed]"

def test():
        print "\nTest~~~~ end"
        bucket = conn.create_bucket('mymy')
        bucket.set_canned_acl('private')        

try:
        eval(sys.argv[1] + '()')
except IndexError:
        help()
except NameError:
        help()


